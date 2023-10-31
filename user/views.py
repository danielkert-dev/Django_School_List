from django.shortcuts import render, redirect
from . import forms
from .forms import ProfilePasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . import models

# Create your views here.
def signin(request):
    if request.method == 'POST':
        form = forms.LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = forms.LoginForm()
    return render(request, 'auth/signin.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = forms.UserCreationFormEdit(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                models.UserProfile.objects.create(user=user)  # This will create the UserProfile

            messages.success(request, f'Account created for {username}')
            return redirect('/')
    else:
        form = forms.UserCreationFormEdit()
    return render(request, 'auth/signup.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def profile(request):
    user_form = forms.CustomUserChangeForm(instance=request.user)
    password_form = forms.ProfilePasswordChangeForm(request.user)
    profile_form = forms.UserProfileForm()

    if request.method == 'POST' and 'update_profile' in request.POST:
        user_form = forms.CustomUserChangeForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')

    if request.method == 'POST' and 'change_password' in request.POST:
        password_form = forms.ProfilePasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            password_form.save()
            messages.success(request, 'Password updated successfully.')
            return redirect('profile')
        
    if request.method == 'POST' and 'user_profile' in request.POST:
        profile_form = forms.UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Image updated successfully.')
            return redirect('profile')


    return render(request, 'auth/profile.html', {'user_form': user_form, 'password_form': password_form, 'profile_form': profile_form})
