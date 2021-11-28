from django.contrib.admin.sites import DefaultAdminSite
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.shortcuts import reverse
from django.db.models.signals import pre_save
from django.dispatch import receiver
import datetime
from django import forms
GENDER_CHOICES = (
    ("1", "Male"),
    ("2", "Female"),
    ("3", "Others"),
)


class Employee(models.Model):
    firstname = models.CharField(default='firstname', max_length=30)
    lastname = models.CharField(default='lastname', max_length=30)
    email = models.CharField(default="", max_length=50)
    user = models.OneToOneField(User, default="", on_delete=models.CASCADE)
    empid = models.IntegerField(default=1234, primary_key=True)
    ismanager = models.IntegerField(default=0)


class Attendance(models.Model):
    employee = models.OneToOneField(
        Employee, default="", on_delete=models.CASCADE, primary_key=True)
    attendance = models.IntegerField(default=0)
    lastupdated = models.DateField(default=datetime.date(2001, 8, 1))


class Team_Detail(models.Model):
    teamname = models.CharField(default='Team 1', max_length=30)
    teamid = models.AutoField(primary_key=True)
    manager = models.ForeignKey(Employee, default="", on_delete=models.CASCADE)


class Team_Member(models.Model):
    employee = models.ForeignKey(
        Employee, default="", on_delete=models.CASCADE)
    team = models.ForeignKey(Team_Detail, on_delete=models.CASCADE)


class Account_Detail(models.Model):
    employee = models.OneToOneField(
        Employee, default="", on_delete=models.CASCADE, primary_key=True)
    Account_Id = models.CharField(null=True, blank=True, max_length=30)
    IFSC_Code = models.CharField(null=True, blank=True, max_length=30)
    Account_Name = models.CharField(null=True, blank=True, max_length=30)


class Project_Detail(models.Model):
    Name = models.CharField(default="", max_length=30)
    Status = models.IntegerField(default=0)
    team = models.ForeignKey(Team_Detail, on_delete=models.CASCADE)
    Project_Description = models.TextField(default="")


class Chat_Message(models.Model):
    Time = models.DateTimeField()
    Sender = models.ForeignKey(Employee, default="", on_delete=models.CASCADE)
    Receiver = models.IntegerField(default=0)
    Message = models.TextField(default="")


class Noticeboard(models.Model):
    date = models.DateField()
    manager = models.ForeignKey(Employee, default="", on_delete=models.CASCADE)
    content = models.TextField(default="")


class Leave_Application(models.Model):
    date_applied = models.DateField()
    date_from = models.DateField()
    date_till = models.DateField()
    reason = models.TextField(default="")
    Sender = models.ForeignKey(Employee, default="", on_delete=models.CASCADE)
    Status = models.IntegerField(default=0)
    request_id = models.AutoField(primary_key=True)
