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
def download(request):
    return render(request, 'download.html')

# View for the login page
def index(request):
    return render(request, 'index.html')

# View for user login
class CustomLoginView(LoginView):
    template_name = 'login.html'

# View for user signup
def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# View for user logout
class CustomLogoutView(LogoutView):
    next_page = 'home'

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