from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from .forms import RegisterForm
from .models import User, Student
# Create your views here.

def register(request):
    # post request means registration form has been submitted
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # save user to database
            form.save()
            messages.success(request, 'Account created successfully!')
            # check if the user is a student or a teacher
            role = form.cleaned_data['role']
            if role == 'STUDENT':
                return redirect('user:login')
            
            elif role == 'TEACHER':
                return redirect('user:login')
        else:
            return render(request, 'user/register.html', {'form': form})

    form = RegisterForm()
        
    return render(request, 'user/register.html', {'form': form})

