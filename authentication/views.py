from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import auth
from django import forms
from organisation.models import Account_Detail, Attendance, Employee
from authentication.models import UserForm
import datetime


def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            newuser = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            firstname = form.cleaned_data.get('firstname')
            lastname = form.cleaned_data.get('lastname')
            #dob = form.cleaned_data.get('dob')

            raw_password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password=raw_password)
            user.save()
            user_id = user.id
            employee = Employee(user=user, firstname=firstname,
                                lastname=lastname, email=email, empid=user_id).save()
            Attendance(employee=employee, attendance=0,
                       employee_id=user_id).save()
            Account_Detail(employee=employee, employee_id=user_id).save()

            newuser.save()
            login(request, user)
            return redirect('index')
    elif request.user.is_authenticated:
        return redirect('profile')
    else:
        form = UserForm()
    return render(request, 'registration/register.html', {'form': form})


def logout(request):
    auth.logout(request)
    return redirect('index')
