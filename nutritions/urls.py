from django.contrib import admin
from django.urls import path
from nutritions import views
urlpatterns = [
    path('', views.main_page, name='main_page' ),
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('logout/', views.logout_page, name='logout'),
    path('userinfo/', views.info_gathering_page, name='userinfo'),
    path('settings/', views.settings_page, name='settings'),
    path('edit/', views.edit_page, name='edit'),
    path('settings/disablenotifications/', views.disableNotifications, name='disablenotifications'),
    path('mealPage/', views.meal_plan_page, name='meal_plan'),
    path('mealPageGeneration/', views.generated_mealPlan_page, name='generated_meal_plan'),
]
