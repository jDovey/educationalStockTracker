from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from user.models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']