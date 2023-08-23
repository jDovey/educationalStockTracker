from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages

# import timezone and datetime for password age check
from django.utils import timezone
import datetime

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.username == "admin":
                return redirect('admin:index')
            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, 'You are not authorized to view this page.')
                if request.user.role == "TEACHER":
                    return redirect('classroom:teacher')
                
                return redirect('core:index')
        return wrapper_func
    return decorator

def passwordAgeCheck():
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.passwordTimeSet < timezone.now() - datetime.timedelta(days=180):
                messages.error(request, 'Your password is too old. Please change it.')
                return redirect('user:change_password')
            else:
                return view_func(request, *args, **kwargs)
        return wrapper_func
    return decorator

