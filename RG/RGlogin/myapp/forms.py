from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    
    class Meta:
        model = User 
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email

class CustomAuthenticationForm(AuthenticationForm):
    username_or_email = forms.CharField(label='Username or Email')

    def clean(self):
        username_or_email = self.cleaned_data.get('username_or_email')
        password = self.cleaned_data.get('password')

        # Check if the input is a valid email
        try:
            email = forms.EmailField().clean(username_or_email)
        except forms.ValidationError:
            email = None

        if email:
            # If the input is an email, try to get the corresponding username
            try:
                user = User.objects.get(email=email)
                self.cleaned_data['username'] = user.username
            except User.DoesNotExist:
                raise forms.ValidationError("No user with this email.")
        else:
            # If the input is not an email, treat it as a username
            self.cleaned_data['username'] = username_or_email

        return super().clean()
