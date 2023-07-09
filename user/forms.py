from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

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

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']