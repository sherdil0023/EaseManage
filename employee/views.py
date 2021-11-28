from django.contrib.auth import authenticate, login
from django.db.models import manager
from django.db.models.query import RawQuerySet
from django.views.decorators import csrf
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
# Create your views here.
from django.http import HttpResponse, JsonResponse
from organisation.models import *
from django.core.serializers.json import DjangoJSONEncoder
import datetime
import json


@login_required
def home(request):
    return render(request, "pages/home.html", {'ismanager': ismanager(request.user)})


@login_required
@csrf_exempt
def messages(request):
    Emp = Employee.objects.filter(user=request.user)[0]
    teams_of_employee = Team_Member.objects.filter(employee=Emp)
    related_employees = Employee.objects.none()
    for team_member in teams_of_employee:
        other_emps = Team_Member.objects.filter(team=team_member.team)
        for emp_member in other_emps:
            if emp_member.employee != Emp:
                related_employees = related_employees | Employee.objects.filter(
                    empid=emp_member.employee.empid)

    if request.method == "GET" and request.GET.get('flag') == '1':

        x = request.GET.get('x')
        y = request.GET.get('y')
        senderobj = Employee.objects.filter(empid=y)[0]
        messages1 = Chat_Message.objects.filter(Sender=senderobj, Receiver=x)
        messages2 = Chat_Message.objects.filter(Sender=Emp, Receiver=y)

        messages = messages1.union(messages2).order_by('id')
        messages = messages.values()
 
        for msg in messages:
            msg["Time"] = msg["Time"].strftime("%m/%d/%Y, %H:%M:%S")
        messages_json = list(messages)

        return JsonResponse(messages_json, safe=False)
    elif request.method == 'POST':
        id = request.POST.get('receiverid')
        empid = request.POST.get('senderid')
        senderobj = Employee.objects.filter(empid=empid)[0]
        message = request.POST.get('message')
        time = datetime.datetime.now()

        Chat_Message.objects.create(
            Sender=senderobj, Receiver=id, Time=time, Message=message).save()
        return render(request, "pages/chat.html", {'users': related_employees, 'ismanager': ismanager(request.user)})
    else:
        return render(request, "pages/chat.html", {'users': related_employees, 'ismanager': ismanager(request.user)})


@login_required
@csrf_exempt
def mesages(request):

    if request.method == 'POST':
        id = request.POST.get('receiverid')
        empid = request.POST.get('senderid')
        senderobj = Employee.objects.filter(empid=empid)[0]
        message = request.POST.get('message')
        time = datetime.datetime.now()
        Chat_Message.objects.create(
            Sender=senderobj, Receiver=id, Time=time, Message=message).save()

    Emp = Employee.objects.filter(user=request.user)[0]
    teams_of_employee = Team_Member.objects.filter(employee=Emp)
    related_employees = Employee.objects.none()
    for team_member in teams_of_employee:
        other_emps = Team_Member.objects.filter(team=team_member.team)
        for emp_member in other_emps:
            if emp_member.employee != Emp:
                related_employees = related_employees | Employee.objects.filter(
                    empid=emp_member.employee.empid)

    empid = request.user.id
    senderobj = Employee.objects.filter(empid=empid)[0]
    messages = Chat_Message.objects.filter(
        Sender=senderobj) | Chat_Message.objects.filter(Receiver=empid)
    messages_json = messages.values_list()
    lis = []
    for ele in messages_json:
        sender = Employee.objects.filter(empid=ele[2])[0]
        receiver = Employee.objects.filter(empid=ele[3])[0]
        if sender not in lis:
            lis.append(sender)
        if receiver not in lis:
            lis.append(receiver)
    if senderobj in lis:
        lis.remove(senderobj)

    messages_json = json.dumps(list(messages_json), cls=DjangoJSONEncoder)
    # print(messages_json)

    return render(request, "pages/chat.html", {'array': messages, 'messages_json': messages_json, 'users': related_employees, 'ismanager': ismanager(request.user)})


@csrf_exempt
@login_required
def attendance(request):

    today = datetime.date.today()
    dt = datetime.date(2021, 8, 1)
    delta = (today-dt)
    passed = delta.days
    employee = Employee.objects.filter(user=request.user)
    dayjoined = request.user.date_joined
    dtt = datetime.date(2021, 8, 1)
    delta = dayjoined.date()-dtt
    dayspassed = passed - delta.days + 1
    if request.method == "GET":
        attend = Attendance.objects.get(employee=employee[0])
        daysattended = attend.attendance
        daysattended_json = json.dumps(daysattended, cls=DjangoJSONEncoder)
        dayspassed_json = json.dumps(dayspassed, cls=DjangoJSONEncoder)
        return render(request, 'pages/attendance.html', {'daysattended_json': daysattended_json, 'dayspassed_json': dayspassed_json, 'ismanager': ismanager(request.user)})
    elif request.method == "POST":
        attend = Attendance.objects.get(employee=employee[0])
        var = attend.attendance
        if attend.lastupdated != datetime.date.today():
            var += 1
            attend.attendance = var
            attend.lastupdated = datetime.date.today()
            attend.save()
        daysattended = var
        daysattended_json = json.dumps(daysattended, cls=DjangoJSONEncoder)
        dayspassed_json = json.dumps(dayspassed, cls=DjangoJSONEncoder)
        return render(request, 'pages/attendance.html', {'daysattended_json': daysattended_json, 'dayspassed_json': dayspassed_json, 'ismanager': ismanager(request.user)})


@csrf_exempt
def myteams(request):
    employee = Employee.objects.filter(user=request.user)[0]
    if request.user.is_authenticated:
        if request.method == 'GET':
            teammembers = Team_Member.objects.filter(employee=employee)
            teams = Team_Detail.objects.none()
            allteams = Team_Detail.objects.all()
            for team in allteams:
                if len(Team_Member.objects.filter(employee=employee, team=team)) == 0:
                    teams = teams | Team_Detail.objects.filter(
                        teamid=team.teamid)
            return render(request, 'pages/myteams.html', {'teammembers': teammembers, 'teams': teams, 'ismanager': ismanager(request.user)})
        elif request.method == 'POST':
            flag = request.POST.get('flag')
            if flag == '0':
                team = Team_Detail.objects.filter(
                    teamid=request.POST.get('code'))
                if len(team) == 1:
                    isinteam = Team_Member.objects.filter(
                        employee=employee, team=team[0])
                    if len(isinteam) == 0:
                        Team_Member.objects.create(
                            employee=employee, team=team[0]).save()
                else:
                    print("Error")
            else:
                leave_id = request.POST.get('id_team')
                team_leave = Team_Detail.objects.filter(teamid=leave_id)[0]
                Team_Member.objects.filter(
                    employee=employee, team=team_leave).delete()
            teammembers = Team_Member.objects.filter(employee=employee)
            return render(request, 'pages/myteams.html', {'teams': teammembers, 'ismanager': ismanager(request.user)})
    else:
        return redirect('index')


def ismanager(user):
    employee = Employee.objects.filter(user=user)
    if len(employee) == 0:
        return False
    emp = employee[0]
    if emp.ismanager == 0:
        return False
    else:
        return True


@csrf_exempt
@login_required
def join_employee(request):
    employee = Employee.objects.get(user=request.user)
    teammembers = Team_Member.objects.filter(employee=employee[0])
    if request.method == "GET":
        teams_json = teammembers.values_list()
        teams_json = json.dumps(list(teams_json), cls=DjangoJSONEncoder)
        if teammembers.count() > 0:
            return render(request, 'pages/myteams.html', {'teams': teammembers, 'itm': teams_json, 'ismanager': ismanager(request.user)})
        return render(request, 'pages/myteams.html', {'message': "No Team to show", 'ismanager': ismanager(request.user)})


@csrf_exempt
def createteam(request):
    employee = Employee.objects.get(user=request.user)
    if request.method == 'GET':
        return render(request, 'pages/createteam.html', {'ismanager': ismanager(request.user)})
    elif request.method == 'POST':
        team = Team_Detail.objects.create(
            teamname=request.POST.get('TeamName'), manager=employee)
        Team_Member.objects.create(
            team=team, employee=employee, team_id=team.teamid).save()
        team.save()
        Team_Member.objects.filter()
        teammembers = Team_Member.objects.filter(employee=employee)
        return render(request, 'pages/teamscreated.html', {'teams': teammembers, 'ismanager': ismanager(request.user)})


def teamscreated(request):
    employee = Employee.objects.get(user=request.user)
    teams = Team_Detail.objects.filter(manager=employee)
    teams_json = teams.values_list()
    teams_json = json.dumps(list(teams_json), cls=DjangoJSONEncoder)
    return render(request, 'pages/teamscreated.html', {'team': teams, 'team_json': teams_json, 'ismanager': ismanager(request.user)})


@csrf_exempt
def editteam(request):
    employee = Employee.objects.filter(user=request.user)[0]
    if request.method == 'GET':
        redirect('teamscreated')
    elif request.method == 'POST':
        team = Team_Detail.objects.get(teamid=request.POST.get('teamid'))
        team.teamname = request.POST.get('teamname')
        team.save()
        redirect('teamscreated')


@csrf_exempt
def deleteteam(request):
    employee = Employee.objects.filter(user=request.user)[0]
    if request.method == 'GET':
        redirect('teamscreated')
    elif request.method == 'POST':
        team = Team_Detail.objects.get(teamid=request.POST.get('teamid'))
        team.delete()
        redirect('teamscreated')


@csrf_exempt
@login_required
def noticeboard(request):
    employee = Employee.objects.filter(user=request.user)[0]
    notices = Noticeboard.objects.none()
    if request.method == "GET":
        employee_teams = Team_Member.objects.filter(employee=employee)
        if ismanager(request.user):
            notices = notices | Noticeboard.objects.filter(manager=employee)
        for x in employee_teams:
            notices = notices | Noticeboard.objects.filter(
                manager=x.team.manager)
        notices = reversed(notices)
        return render(request, "pages/noticeboard.html", {'notices': notices, 'ismanager': ismanager(request.user)})
    elif request.method == "POST" and ismanager(request.user):
        flag = request.POST.get('flag')
        if flag == '0':
            idedit = request.POST.get('noticeid')
            newcontent = request.POST.get('noticecontent')
            notice = Noticeboard.objects.get(id=idedit)
            notice.content = newcontent
            notice.save()
        elif flag == '1':
            iddelete = request.POST.get('noticeid')
            Noticeboard.objects.filter(id=iddelete).delete()
        else:
            content = request.POST.get('content')
            employee = Employee.objects.filter(user=request.user)[0]
            Noticeboard.objects.create(
                manager=employee, date=datetime.date.today(), content=content)
        return render(request, "pages/noticeboard.html", {'notices': notices, 'ismanager': ismanager(request.user)})


@csrf_exempt
@login_required
def leaves(request):
    employee = Employee.objects.filter(user=request.user)[0]
    user_employee = Employee.objects.filter(user=request.user)[0]
    teams = Team_Detail.objects.filter(manager=employee)
    employees = Employee.objects.none()
    leaves = Leave_Application.objects.none()
    for team in teams:
        team_employees = Team_Member.objects.filter(team=team)
        for emp in team_employees:
            if emp.employee != user_employee:
                employees = employees | Employee.objects.filter(
                    empid=emp.employee.empid)
                leaves = leaves | Leave_Application.objects.filter(
                    Sender=emp.employee)
    if request.method == "GET" and not ismanager(request.user):
        leaves = Leave_Application.objects.filter(Sender=employee)
        return render(request, "pages/employee_leaves.html", {'leave_requests': leaves, 'ismanager': ismanager(request.user)})
    elif request.method == "GET" and ismanager(request.user):
        return render(request, "pages/manager_leaves.html", {'leave_requests': leaves, 'ismanager': ismanager(request.user)})
    elif request.method == "POST" and ismanager(request.user):
        modify_type = request.POST.get('modify_type')
        req_id = request.POST.get('req_id')
        leave_app = Leave_Application.objects.get(request_id=req_id)
        if modify_type == '1':
            leave_app.Status = 2
        else:
            leave_app.Status = 1
        leave_app.save()
        return render(request, "pages/manager_leaves.html", {'leave_requests': leaves, 'ismanager': ismanager(request.user)})
    elif request.method == "POST" and not ismanager(request.user):
        from_date = request.POST.get("from_date")
        till_date = request.POST.get("till_date")
        reason = request.POST.get("reason")
        Leave_Application.objects.create(Sender=employee, Status=0, date_applied=datetime.date.today(
        ), date_from=from_date, date_till=till_date, reason=reason)
        leaves = Leave_Application.objects.filter(Sender=employee)
        return render(request, "pages/employee_leaves.html", {'leave_requests': leaves, 'ismanager': ismanager(request.user)})
    return render(request, "pages/leaves.html")


@csrf_exempt
@login_required
def profilepage(request):
    if request.method == "GET":
        employee = Employee.objects.filter(user=request.user)[0]
        return render(request, "pages/profilepage.html", {'employee': employee, 'ismanager': ismanager(request.user)})
    elif request.method == "POST":
        flag = request.POST.get('flag')
        if flag == '1':
            employee = Employee.objects.get(user=request.user)
            employee.firstname = request.POST.get('value')
            employee.save()
        elif flag == '2':
            employee = Employee.objects.get(user=request.user)
            employee.lastname = request.POST.get('value')
            employee.save()
        elif flag == '3':
            employee = Employee.objects.get(user=request.user)
            employee.email = request.POST.get('value')
            user = request.user
            user.email = employee.email
            user.save()
            employee.save()
        elif flag == '4':
            user = request.user
            user.set_password(request.POST.get('pwd'))
            user.save()
        employee = Employee.objects.filter(user=request.user)[0]
        return render(request, "pages/profilepage.html", {'employee': employee, 'ismanager': ismanager(request.user)})


@csrf_exempt
@login_required
def profilesalary(request):
    emp = Employee.objects.filter(user=request.user)[0]
    teams = Team_Detail.objects.filter(manager=emp)
    account_detail = Account_Detail.objects.filter(employee=emp)[0]
    if request.method == "GET":
        return render(request, "pages/profileaccounts.html", {'ismanager': ismanager(request.user), 'acc_det': account_detail})
    elif request.method == "POST":
        flag = request.POST.get('flag')
        emp = Employee.objects.filter(user=request.user)[0]
        detail = Account_Detail.objects.get(employee=emp)
        if flag == '1':
            newacc = request.POST.get('value')
            detail.Account_Id = newacc
        elif flag == '2':
            newIFSC = request.POST.get('value')
            detail.IFSC_Code = newIFSC
        elif flag == '3':
            newname = request.POST.get('value')
            detail.Account_Name = newname
        detail.save()
        return render(request, "pages/profileaccounts.html", {'ismanager': ismanager(request.user), 'acc_det': account_detail})


@csrf_exempt
@login_required
def projects(request):
    employee = Employee.objects.filter(user=request.user)[0]
    projects = Project_Detail.objects.none()
    if ismanager(request.user) and request.method == "GET":
        teams = Team_Detail.objects.filter(manager=employee)
        for team in teams:
            projects = projects | Project_Detail.objects.filter(team=team)
        return render(request, "pages/projects.html", {'projects': projects, 'ismanager': ismanager(request.user), 'teams': teams})
    elif request.method == "GET":
        team_members = Team_Member.objects.filter(employee=employee)
        for team_member in team_members:
            projects = projects | Project_Detail.objects.filter(
                team=team_member.team)
        return render(request, "pages/projects.html", {'projects': projects, 'ismanager': ismanager(request.user)})
    elif ismanager(request.user) and request.method == "POST" and request.POST.get("flag") == "1":
        team_id = request.POST.get("team_id")
        project_name = request.POST.get("project_name")
        project_desc = request.POST.get("project_desc")
        team = Team_Detail.objects.filter(teamid=team_id)[0]
        Project_Detail(team=team, Name=project_name,
                       Project_Description=project_desc).save()
        teams = Team_Detail.objects.filter(manager=employee)
        projects = Project_Detail.objects.none()
        for team in teams:
            projects = projects | Project_Detail.objects.filter(team=team)
        return render(request, "pages/projects.html", {'projects': projects, 'ismanager': ismanager(request.user)})
    elif ismanager(request.user) and request.method == "POST" and request.POST.get("flag") == "0":
        project_id = request.POST.get("id")
        project = Project_Detail.objects.get(id=project_id)
        project.Status = 1
        project.save()
        teams = Team_Detail.objects.filter(manager=employee)
        projects = Project_Detail.objects.none()
        for team in teams:
            projects = projects | Project_Detail.objects.filter(team=team)
        return render(request, "pages/projects.html", {'projects': projects, 'ismanager': ismanager(request.user)})
