from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm

from user.models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
        'autofocus': 'autofocus',
        }))
    
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email',
        }))
    
    password1 = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
        }))
    
    password2 = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm Password',
        }))
    
    role = forms.ChoiceField(choices=User.Role.choices, widget=forms.Select(attrs={
        'class': 'form-control',
        }))

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
    
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
        'autofocus': 'autofocus',
        }))

    password = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
        }))
    
class PasswordChangingForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

    old_password = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Old password',
        'autofocus': 'autofocus',
        'type': 'password',
        }))
    
    new_password1 = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'New password',
        'type': 'password',
        }))
    
    new_password2 = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm new password',
        'type': 'password',
        }))
    