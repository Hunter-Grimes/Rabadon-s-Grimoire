from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from . import views
from .forms import SignupForm
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import render

# View for the home page
def home(request):
    timestamp = int(timezone.now().timestamp())
    return render(request, 'home.html', {'timestamp': timestamp})

# View for the about page
def about(request):
    timestamp = int(timezone.now().timestamp())
    return render(request, 'about.html', {'timestamp': timestamp})

# View for the contact page
def contact(request):
    timestamp = int(timezone.now().timestamp())
    return render(request, 'contact.html', {'timestamp': timestamp})

# View for the download page
@login_required
def download(request):
    timestamp = int(timezone.now().timestamp())
    return render(request, 'download.html', {'timestamp': timestamp})

# View for the login page
def custom_login(request):
    timestamp = int(timezone.now().timestamp())
    return render(request, 'login.html', {'timestamp': timestamp})

# View for the logout page
def custom_logout(request):
    logout(request)
    return redirect('home')

# View for user signup
def signup(request):
    timestamp = int(timezone.now().timestamp())
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Check if username already exists
            username = form.cleaned_data.get('username')
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Username already exists')
            else:
                user = form.save()
                user.refresh_from_db()  
                # load the profile instance created by the signal
                user.save()
                raw_password = form.cleaned_data.get('password1')

                # login user after signing up
                user = authenticate(username=user.username, password=raw_password)
                login(request, user)

                # redirect user to home page
                return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form, 'timestamp': timestamp})

# View for initiating password reset
class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset_form.html'

# Password reset done page
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'

# Confirm password reset
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'

# Password reset complete page
class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'