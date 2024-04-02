from importlib.metadata import requires
from django import forms
from django.contrib.auth.forms import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class SignupForm(UserCreationForm):  
    class Meta:
        model = User 
        fields = ['username', 'password1', 'password2']
