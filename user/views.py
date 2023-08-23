from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .forms import RegisterForm, PasswordChangingForm
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

@login_required
def profile(request):
    return render(request, 'user/profile.html')

class CustomPasswordChangeView(auth_views.PasswordChangeView):
    template_name = 'user/change_password.html'
    success_url = '/'
    form_class = PasswordChangingForm
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Password changed successfully!')
        # after changing password, set the passwordTimeSet field to now
        # this is used to check if the password is too old
        self.request.user.passwordTimeSet = timezone.now()
        self.request.user.save()
        return response

@login_required
def deleteAccount(request):
    if request.method == 'POST':
        # delete the user from the database
        request.user.delete()
        messages.success(request, 'Account deleted successfully!')
    return redirect('user:login')