from importlib.metadata import requires
from django import forms
from django.contrib.auth.forms import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].error_messages = {'required': 'Username is required.',
                                                   'min_length': 'Username must be at least 4 characters long.'}
        self.fields['password1'].error_messages = {'required': 'Password is required.',
                                                    'min_length': 'Password must be at least 6 characters long.'}
        self.fields['password2'].error_messages = {'required': 'Confirmation password is required.',
                                                    'min_length': 'Password must be at least 6 characters long.',
                                                    'password_mismatch': 'The two password fields didn\'t match.'}

    class Meta:
        model = User 
        fields = ['username', 'password1', 'password2']