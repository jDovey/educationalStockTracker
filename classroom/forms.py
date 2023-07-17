from django import forms

from .models import Classroom

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
    