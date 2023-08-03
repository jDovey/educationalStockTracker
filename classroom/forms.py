from django import forms

from .models import Classroom, Lesson
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
    
class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('status', 'order', 'title', 'description', 'content', 'image', 'learning_objectives')
    
    status = forms.ChoiceField(choices=Lesson.Status.choices, widget=forms.Select(attrs={
        'class': 'form-control',
        'placeholder': 'Status',
    }))
    
    order = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Order',
    }))
    
    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Title',
    }))
    
    description = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Description',
    }))
    
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Content',
    }))
    
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'class': 'form-control',
        'placeholder': 'Image',
    }))
    
class LearningObjectiveForm(forms.Form):
    class Meta:
        fields = ('learning_objective',)
        
    learning_objective = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Learning Objective',
    }))

LearningObjectiveFormSet = forms.formset_factory(LearningObjectiveForm, extra=0)