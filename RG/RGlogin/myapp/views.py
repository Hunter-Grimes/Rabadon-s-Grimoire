from django.shortcuts import render
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

# View for the home page
def home(request):
    return render(request, 'home.html')

# View for the about page
def about(request):
    return render(request, 'about.html')

# View for the contact page
def contact(request):
    return render(request, 'contact.html')

# View for the download page
@login_required
def download(request):
    return render(request, 'download.html')

# View for the login page
def custom_login(request):
    return render(request, 'login.html')

# View for the logout page
def custom_logout(request):
    logout(request)
    return redirect('home')

# View for user signup
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()

            # Retrieve the entered username or email
            identifier = form.cleaned_data['username_or_email']
            
            # Authenticate user with either username or email
            user = authenticate(request, identifier=identifier, password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

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