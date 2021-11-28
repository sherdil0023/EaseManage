from django.urls import path
from . import views
from django.conf.urls.static import static
from mysite import settings
urlpatterns = [
    path('profile/details', views.profilepage, name='profile'),
    path('profile/', views.home, name='home'),
    path('profile/attendance/', views.attendance, name='attendance'),
    path('profile/myteams/', views.myteams, name='myteams'),
    path('profile/createteam/', views.createteam, name='createteam'),
    path('profile/teamscreated/', views.teamscreated, name='teamscreated'),
    path('profile/editteam/', views.editteam, name="editteam"),
    path('profile/deleteteam', views.deleteteam, name="deleteteam"),
    path('profile/noticeboard', views.noticeboard, name="notices"),
    path('messages/', views.messages, name="chat"),
    path('profile/leaves', views.leaves, name="leaves"),
    path('profile/profilepage', views.profilepage, name="profilepage"),
    path('profile/profilesalary', views.profilesalary, name="profilesalary"),
    path('profile/projects', views.projects, name="projects")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
