from typing import Any
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import UserProfile
from PIL import Image


class UserCreationFormEdit(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Email'
        self.fields['email'].help_text = 'Required. It needs atleast one @ and a . character'
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Confirm Password'
        

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username',
        })

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Email',
        })

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password',
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm Password',
        })

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['password'].label = 'Password'

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username',
        })

        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password',
        })

class ProfilePasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = 'Old Password'
        self.fields['new_password1'].label = 'New Password'
        self.fields['new_password2'].label = 'Confirm New Password'

        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Old Password',
        })

        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'New Password',
        })

        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm New Password',
        })

class CustomUserChangeForm(UserChangeForm):
    new_username = forms.CharField(max_length=150, required=False, label="New Username")

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def clean_new_username(self):
        new_username = self.cleaned_data['new_username']
        if new_username:
            if User.objects.filter(username=new_username).exists():
                raise forms.ValidationError("Username is already in use.")
        return new_username

    def save(self, commit=True):
        user = super().save(commit=False)
        new_username = self.cleaned_data['new_username']
        if new_username:
            user.username = new_username
        if commit:
            user.save()
        return user
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Email address'
        self.fields['new_username'].label = 'New username'

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Email',
        })

        self.fields['new_username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'New username',
        })


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].label = 'Profile Picture'

        self.fields['image'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Profile Picture',
        })