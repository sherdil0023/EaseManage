from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from datetime import date

d0 = date(2021, 8, 21)
d1 = date.today()
delta = d1 - d0


GENDER_CHOICES = (
    ("1", "Male"),
    ("2", "Female"),
    ("3", "Others"),
)


class UserForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    firstname = forms.CharField(label="First name")
    lastname = forms.CharField(label="Last name")
    #dob = forms.DateField(label = "Date Of Birth")
    #gender = forms.MultipleChoiceField(choices = GENDER_CHOICES,label="Gender")

    class Meta:
        model = User
        fields = ("username", "firstname", "lastname", "email")
