from django import forms
from django.core.validators import MinValueValidator

from .models import Holdings

class QuoteForm(forms.Form):
    symbol = forms.CharField(max_length=10, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Symbol',
        'autofocus': 'autofocus',
        }))
    
class BuyForm(forms.Form):
    symbol = forms.CharField(max_length=10, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Symbol',
        'autofocus': 'autofocus',
        }))
    shares = forms.IntegerField(
        validators=[MinValueValidator(1)],
        widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Number of shares',
        }))
    
class SellForm(forms.Form):
    holding = forms.ModelChoiceField(queryset=None, widget=forms.Select(attrs={
        'class': 'form-control',
        'placeholder': 'Holding',
        'autofocus': 'autofocus',
        }))
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Number of shares',
        }))
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(SellForm, self).__init__(*args, **kwargs)
        self.fields['holding'].queryset = Holdings.objects.filter(student__user=self.request.user)


        
        
