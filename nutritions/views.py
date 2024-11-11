from django.shortcuts import render, redirect
from django.template.context_processors import request

from .models import UserInfo, User, UserSchedule
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
import sqlite3
from django.http import JsonResponse
import json


def main_page(request):
    if request.user.is_authenticated:
        user_info = UserInfo.objects.get(user=User.objects.get(username=request.user))
        user_schedule = UserSchedule.objects.filter(user_info=user_info)
        if user_schedule.exists():
            return render(request, "main_page.html", {'user_info': user_info, "user_schedule": UserSchedule.objects.get(user_info=user_info)})
        else:
            return render(request, "main_page.html", {'user_info': user_info, "user_schedule": 0})
    return render(request, "main_page.html", {'user_info': 'noinfo'})

def login_page(request):
    if request.user.is_authenticated:
        return redirect('main_page')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')  # Redirect to a home page or desired page after login
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    return redirect('/')


def register_page(request):
    if request.user.is_authenticated:
        return redirect(main_page)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password != password_confirm:
            messages.error(request, 'Passwords do not match')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        else:
            user = User.objects.create_user(username=username, password=password)
            user_instance = UserInfo.objects.create(user=user)
            UserSchedule.objects.create(user_info=user_instance)
            login(request, user)  # Automatically log in the user after registration
            return redirect('/')  # Redirect to a homepage after registration

    return render(request, 'registration.html')

def calculate_BMR(age, weight, height, gender,prefference):
    # Connect to the SQLite database
    conn = sqlite3.connect('meals.sqlite3')
    cursor = conn.cursor()

    # Query to get calories from the breakfast table
    cursor.execute("SELECT CalorieValue FROM breakfast")
    # Fetch all results and store them in a list
    calories_list = [row[0] for row in cursor.fetchall()]
    if gender == 1:  # Male

        BMR = (10 * weight + 6.25 * height - 5 * age + 5) * 0.45+prefference*315
    else:  # Female
        BMR = (10 * weight + 6.25 * height - 5 * age - 161) * 0.45+prefference*315

    # Find the closest calorie value
    closest_calories = min(calories_list, key=lambda x: abs(x - BMR))

    # Query to get the ID where the CalorieValue is closest to BMR
    cursor.execute("SELECT ID FROM breakfast WHERE CalorieValue = ?", (closest_calories,))
    row_uni = cursor.fetchone()  # Fetch the first matching row
    if row_uni:
        ID = row_uni[0]  # ID of the corresponding row
    else:
        return []  # Return empty if no matching calorie value

    # List to store results
    result_list = []

    # Fetch Option1, Option2, and Option3 from each meal table in sequence
    for option in range(1, 4):  # Option1, Option2, Option3
        for meal in ['breakfast', 'lunch', 'dinner']:
            cursor.execute(f"SELECT Option{option} FROM {meal} WHERE ID = ?", (ID,))
            option_value = cursor.fetchone()
            if option_value:
                result_list.append(option_value[0])
    # Append the actual value
    # Check if the result list is not empty
    if result_list:
        # Repeat the first 9 elements until the list reaches 21 elements
        while len(result_list) < 21:
            result_list.extend(result_list[:9])  # Append the first 9 elements

        # Trim the list to exactly 21 elements in case it exceeds
        result_list = result_list[:21]
    conn.close()
    return result_list

# INFO GATHERING
def info_gathering_page(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            age = request.POST.get('age')
            weight = request.POST.get('weight')
            height = request.POST.get('height')
            gender = request.POST.get('gender')
            preference = request.POST.get('preference')
            user_info = UserInfo.objects.get(user=User.objects.get(username=request.user))
            user_info.age = age
            user_info.weight = weight
            user_info.height = height
            user_info.gender = gender
            user_info.preference = preference
            user_info.save()
            return redirect('/mealPageGeneration/')
        return render(request, "info_gathering_page.html")
    return redirect(main_page)


def settings_page(request):
    if request.user.is_authenticated:
        user_info = UserInfo.objects.get(user=User.objects.get(username=request.user))
        return render(request, 'settings_page.html', {'user_info':user_info})
    return redirect(main_page)

def edit_page(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            age = request.POST.get('age')
            weight = request.POST.get('weight')
            height = request.POST.get('height')
            gender = request.POST.get('gender')
            preference = request.POST.get('preference')
            user_info = UserInfo.objects.get(user=User.objects.get(username=request.user))
            user_info.age = age
            user_info.weight = weight
            user_info.height = height
            user_info.gender = gender
            user_info.preference = preference
            user_info.save()
            return redirect('/mealPageGeneration/')
        return render(request, "edit_page.html")
    return redirect(main_page)

def disableNotifications(request):
    if request.user.is_authenticated:
        user_info = UserInfo.objects.get(user=User.objects.get(username=request.user))
        user_info.telegram_id = 0
        user_info.save()
        return redirect(settings_page)
    return redirect(main_page)

def generated_mealPlan_page(request):
    if request.user.is_authenticated:
        user_info = UserInfo.objects.get(user=User.objects.get(username=request.user))
        user_schedule = UserSchedule.objects.filter(user_info=user_info)
        gender = user_info.gender
        age = user_info.age
        weight = user_info.weight
        height = user_info.height
        preference = int(user_info.preference)
        result = calculate_BMR(age, weight, height, gender, preference)
        if user_schedule.exists():
            user_schedule = UserSchedule.objects.get(user_info=user_info)
            user_schedule.monday_break=result[0]
            user_schedule.monday_lunch=result[1],
            user_schedule.monday_dinner=result[2],
            user_schedule.tuesday_break=result[3],
            user_schedule.tuesday_lunch=result[4],
            user_schedule.tuesday_dinner=result[5],
            user_schedule.wednesday_break=result[6],
            user_schedule.wednesday_lunch=result[7],
            user_schedule.wednesday_dinner=result[8],
            user_schedule.thursday_break=result[9],
            user_schedule.thursday_lunch=result[10],
            user_schedule.thursday_dinner=result[11],
            user_schedule.friday_break=result[12],
            user_schedule.friday_lunch=result[13],
            user_schedule.friday_dinner=result[14],
            user_schedule.saturday_break=result[15],
            user_schedule.saturday_lunch=result[16],
            user_schedule.saturday_dinner=result[17],
            user_schedule.sunday_break=result[18],
            user_schedule.sunday_lunch=result[19],
            user_schedule.sunday_dinner=result[20]
            user_schedule.save()
            '''
            UserSchedule.objects.update(user_info=user_info,
                                    monday_break=result[0],
                                    monday_lunch=result[1],
                                    monday_dinner=result[2],
                                    tuesday_break=result[3],
                                    tuesday_lunch=result[4],
                                    tuesday_dinner=result[5],
                                    wednesday_break=result[6],
                                    wednesday_lunch=result[7],
                                    wednesday_dinner=result[8],
                                    thursday_break=result[9],
                                    thursday_lunch=result[10],
                                    thursday_dinner=result[11],
                                    friday_break=result[12],
                                    friday_lunch=result[13],
                                    friday_dinner=result[14],
                                    saturday_break=result[15],
                                    saturday_lunch=result[16],
                                    saturday_dinner=result[17],
                                    sunday_break=result[18],
                                    sunday_lunch=result[19],
                                    sunday_dinner=result[20])'''
        else:
            UserSchedule.objects.create(user_info=user_info,
                                    monday_break=result[0],
                                    monday_lunch=result[1],
                                    monday_dinner=result[2],
                                    tuesday_break=result[3],
                                    tuesday_lunch=result[4],
                                    tuesday_dinner=result[5],
                                    wednesday_break=result[6],
                                    wednesday_lunch=result[7],
                                    wednesday_dinner=result[8],
                                    thursday_break=result[9],
                                    thursday_lunch=result[10],
                                    thursday_dinner=result[11],
                                    friday_break=result[12],
                                    friday_lunch=result[13],
                                    friday_dinner=result[14],
                                    saturday_break=result[15],
                                    saturday_lunch=result[16],
                                    saturday_dinner=result[17],
                                    sunday_break=result[18],
                                    sunday_lunch=result[19],
                                    sunday_dinner=result[20]).save()
        return redirect('/mealPage/')
    return redirect('/login/')

def meal_plan_page(request):
    if request.user.is_authenticated:
        user_info = UserInfo.objects.get(user=User.objects.get(username=request.user))
        user_schedule = UserSchedule.objects.filter(user_info=user_info)
        if user_schedule.exists():
            return render(request, 'meal_plan.html', {"user_schedule": UserSchedule.objects.get(user_info=user_info)})
        else:
            return redirect('/mealPageGeneration/')
    return redirect('/login/')


