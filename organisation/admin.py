from django.contrib import admin
from .models import *

admin.site.register(Team_Member)
admin.site.register(Noticeboard)
admin.site.register(Project_Detail)
admin.site.register(Chat_Message)
admin.site.register(Account_Detail)
admin.site.register(Leave_Application)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("empid", "firstname", "lastname")


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("employee_id", "attendance")


@admin.register(Team_Detail)
class Team_DetailAdmin(admin.ModelAdmin):
    list_display = ("teamid", "teamname")
