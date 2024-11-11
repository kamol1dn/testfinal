import os
import django
import telebot
import schedule
import time
import threading
import datetime
from datetime import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth import authenticate
import requests


# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HackProj.settings')
django.setup()

from nutritions.models import User, UserInfo, UserSchedule


API_KEY = '7830840669:AAF69IRMrusjVQuKssAjAmQCnPUD1seG1g0'
bot = telebot.TeleBot(API_KEY, parse_mode=None)

# Dictionary to temporarily store logged-in users' data
logged_in_users = {}

def day_set(telegram_id, dayNum, daytime):
    days = {
        1: "monday",
        2: "tuesday",
        3: "wednesday",
        4: "thursday",
        5: "friday",
        6: "saturday",
        7: "sunday"
    }
    dayTimes = {
        1 : "break",
        2 : "lunch",
        3 : "dinner"
    }

    # Construct the attribute name (e.g., "monday_dinner")
    day_name = days[dayNum]
    daytimeFINISH = dayTimes[daytime]
    attribute_name = f"{day_name}_{daytimeFINISH}"  # e.g., "monday_dinner"

    try:
        # Retrieve the schedule for the user based on telegram_id
        user_info = UserInfo.objects.get(telegram_id=telegram_id)
        user_schedule = UserSchedule.objects.get(user_info=user_info)

        # Use getattr to dynamically get the attribute value
        meal_info = getattr(user_schedule, attribute_name, None)

        if meal_info is not None:
            return meal_info
        else:
            return "Meal information not available for this day and time."

    except UserInfo.DoesNotExist:
        return "User info not found."
    except UserSchedule.DoesNotExist:
        return "User schedule not found."


def User_Object(username):
    user = User.objects.get(username=username)
    user1 = UserInfo.objects.get(user=user)
    user2 = UserSchedule.objects.get(user_info=user1)
    return user2


def send_meal_message(chat_id, message_text):
    bot.send_message(chat_id, message_text)

def send_breakfast():
    for user_info in UserInfo.objects.all().values():
        if user_info['telegram_id'] == 0:
            pass
        telegram_id = user_info['telegram_id']
        try:
            current_date = datetime.now()
            day_of_week = current_date.isoweekday()

            message = f"Good morning! Here’s your breakfast:\n{day_set(telegram_id, day_of_week, 1)}"
            send_meal_message(telegram_id, message)
        except UserSchedule.DoesNotExist:
            pass

def send_lunch():
    for user_info in UserInfo.objects.all().values():
        if user_info['telegram_id'] == 0:
            pass
        telegram_id = user_info['telegram_id']
        try:

            current_date = datetime.now()
            day_of_week = current_date.isoweekday()

            message = f"Good afternoon! Here’s your lunch:\n{day_set(telegram_id, day_of_week, 2)}"
            send_meal_message(telegram_id, message)
        except UserSchedule.DoesNotExist:
            pass

def send_dinner():
    for user_info in UserInfo.objects.all().values():
        if user_info['telegram_id'] == 0:
            pass
        telegram_id = user_info['telegram_id']
        try:


            current_date = datetime.now()
            day_of_week = current_date.isoweekday()

            message = f"Good evening! Here’s your dinner:\n{day_set(telegram_id, day_of_week, 3)}"
            send_meal_message(telegram_id, message)
        except UserSchedule.DoesNotExist:
            pass


def send_shopping_list():
    for user_info in UserInfo.objects.all().values():
        if user_info['telegram_id'] == 0:
            pass
        telegram_id = user_info['telegram_id']
        #AI implementation needed

# Bot Command to Start the Bot
@bot.message_handler(commands=['start'])
def start(msg):
    chat_id = msg.chat.id
    if UserInfo.objects.filter(telegram_id=chat_id).exists():
        bot.send_message(chat_id, "Hello, wait for your Notifications")
    else:
        bot.reply_to(msg, "Hello! Type /login to log in to your account.")

# Bot Command to Begin Login Process
@bot.message_handler(commands=['login'])
def login(msg):
    if UserInfo.objects.filter(telegram_id=msg.chat.id).exists():
        bot.send_message(msg.chat.id, "You are already logged in.")
    else:
        chat_id = msg.chat.id
        bot.reply_to(msg, "Enter Your Username:")
        bot.register_next_step_handler(msg, process_username)

@bot.message_handler(commands=['logout'])
def logout(msg):
    user_info = UserInfo.objects.filter(telegram_id=msg.chat.id)
    if user_info.exists():
        user_info = UserInfo.objects.get(telegram_id=msg.chat.id)
    if user_info.telegram_id != 0:
        user_info.telegram_id = 0
        user_info.save()
        bot.reply_to(msg, "Logged Out!")
    else:
        bot.reply_to(msg, "You are not even logged in")

def process_username(msg):
    chat_id = msg.chat.id
    username = msg.text
    logged_in_users[chat_id] = {'username':username}  # Temporarily store username
    bot.reply_to(msg, "Enter Your Password:")
    bot.register_next_step_handler(msg, process_password, username)

def process_password(msg, username):
    chat_id = msg.chat.id
    password = msg.text
    # Authenticate user
    user = authenticate(username=username, password=password)
    try:
        user_info = UserInfo.objects.get(user=user)
        if user_info.telegram_id != 0:
            bot.send_message(chat_id, "This account is already logged in another device.")
            return 0
    except UserInfo.DoesNotExist:
        bot.reply_to(msg, "User does not exist.")
    if user is not None:
        try:
            user_info.telegram_id = msg.chat.id
            user_info.save()
            bot.reply_to(msg, "Login successful! You will now receive meal reminders.")
        except UserInfo.DoesNotExist:
            bot.reply_to(msg, "User information not found.")
    else:
        bot.reply_to(msg, "Invalid username or password.")
        logged_in_users.pop(chat_id, None)  # Remove entry if login failed






# Function to run the schedule in a separate thread
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(60)

# Define the Command Class
class Command(BaseCommand):
    help = "Runs the Telegram bot to send meal notifications"

    def handle(self, *args, **kwargs):
        # Schedule the tasks
        schedule.every().day.at("08:00").do(send_breakfast)
        schedule.every().day.at("13:00").do(send_lunch)
        schedule.every().day.at("19:00").do(send_dinner)
        schedule.every().monday.at("08:30").do(send_shopping_list)

        # Start the schedule in a new thread
        schedule_thread = threading.Thread(target=run_schedule)
        schedule_thread.start()

        # Start polling
        print("Bot started and schedule initialized.")
        bot.polling()
