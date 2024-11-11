from django.db import models
from django.contrib.auth.models import User


# First table: UserInfo model
class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    telegram_id = models.IntegerField(default=0)
    name = models.CharField(max_length=100, default='NoName')
    age = models.IntegerField(default=0)
    weight = models.FloatField(default=0)
    height = models.FloatField(default=0)
    gender = models.CharField(default="NoInfo", max_length=10)
    preference = models.IntegerField(default=0)

    def __str__(self):
        return self.name


# Second table: UserSchedule model
class UserSchedule(models.Model):
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='schedules')
    monday_break = models.CharField(max_length=200, default='none')
    monday_lunch = models.CharField(max_length=200, default='none')
    monday_dinner = models.CharField(max_length=200, default='none')
    tuesday_break = models.CharField(max_length=200, default='none')
    tuesday_lunch = models.CharField(max_length=200, default='none')
    tuesday_dinner = models.CharField(max_length=200, default='none')
    wednesday_break = models.CharField(max_length=200, default='none')
    wednesday_lunch = models.CharField(max_length=200, default='none')
    wednesday_dinner = models.CharField(max_length=200, default='none')
    thursday_break = models.CharField(max_length=200, default='none')
    thursday_lunch = models.CharField(max_length=200, default='none')
    thursday_dinner = models.CharField(max_length=200, default='none')
    friday_break = models.CharField(max_length=200, default='none')
    friday_lunch = models.CharField(max_length=200, default='none')
    friday_dinner = models.CharField(max_length=200, default='none')
    saturday_break = models.CharField(max_length=200, default='none')
    saturday_lunch = models.CharField(max_length=200, default='none')
    saturday_dinner = models.CharField(max_length=200, default='none')
    sunday_break = models.CharField(max_length=200, default='none')
    sunday_lunch = models.CharField(max_length=200, default='none')
    sunday_dinner = models.CharField(max_length=200, default='none')

    def __str__(self):
        return self.user_info.name


