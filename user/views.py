from django.shortcuts import render, redirect
from django.http import HttpResponse

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

            # check if the user is a student or a teacher
            role = form.cleaned_data['role']
            if role == 'STUDENT':
                # create a student object, getting the user by username
                student = Student.objects.create(user=User.objects.get(username=form.cleaned_data.get('username')))
                return HttpResponse('student created')

    form = RegisterForm()
        
    return render(request, 'user/register.html', {'form': form})

def login(request):
    return render(request, 'user/login.html')

def logout(request):
    return render(request, 'user/login.html')
