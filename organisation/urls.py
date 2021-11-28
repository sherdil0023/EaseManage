from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
urlpatterns = [
    path('', LoginView.as_view(redirect_authenticated_user=True), name='index'),
    path('aboutus', views.aboutus, name="about_us"),
    path('profile/managers', views.managers, name='managers')
]
