from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .models import *
import datetime
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.timezone import now
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.utils import datetime_safe
from employee.views import ismanager


@csrf_exempt
def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            return render(request, 'index.html', {'error_message': 'Incorrect username and / or password.'})
    else:
        return render(request, 'index.html')


@csrf_exempt
@login_required
def managers(request):
    if request.user.is_superuser and request.method == 'GET':
        employees = Employee.objects.all()
        return render(request, "managers.html", {'employees': employees, 'ismanager': ismanager(request.user)})
    elif request.user.is_superuser and request.method == 'POST':
        empid = request.POST.get('id')
        emp = Employee.objects.get(empid=empid)
        flag = request.POST.get('flag')
        if flag == '1':
            emp.ismanager = 0
            Team_Detail.objects.filter(manager=emp).delete()
            emp.save()
        else:
            emp.ismanager = 1
            emp.save()
        employees = Employee.objects.all()
        return render(request, "managers.html", {'employees': employees, 'ismanager': ismanager(request.user)})


def aboutus(request):
    return render(request, "about_us.html")
