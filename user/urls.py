from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .forms import LoginForm

app_name = 'user'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password/', views.CustomPasswordChangeView.as_view(template_name='user/change_password.html', success_url='/'), name='change_password'),
    path('profile/', views.profile, name='profile'),
    path('delete/', views.deleteAccount, name='delete_account')
]