from django.urls import path
from authentication.views import signup, logout, login
from django.contrib.auth.views import LoginView
urlpatterns = [
    path('register', signup, name='register'),
    # path('', LoginView.as_view('template_name': 'index.html',redirect_authenticated_user=True), name='index'),

    path('logout', logout, name='logout')

]
