from django.shortcuts import render

# Create your views here.

def register(request):
    return render(request, 'user/register.html')

def login(request):
    return render(request, 'user/login.html')

def logout(request):
    return render(request, 'user/login.html')
