from django import forms

class QuoteForm(forms.Form):
    symbol = forms.CharField(max_length=10, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Symbol',
        'autofocus': 'autofocus',
        }))
    

