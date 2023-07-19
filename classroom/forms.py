from django import forms

from .models import Classroom
from user.models import Student

class NewClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ('name', 'passcode')
        
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Name',
    }))
    
    passcode = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Passcode',
    }))
    
class JoinClassroomForm(forms.Form):
    class Meta:
        fields = ('name', 'passcode')
        
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Name',
    }))
        
    passcode = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Passcode',
    }))
    
class EditStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('cash', 'xp')
        
    cash = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Cash',
    }))
    
    xp = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'XP',
    }))