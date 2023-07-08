from django import forms

class QuoteForm(forms.Form):
    symbol = forms.CharField(label='Symbol', max_length=10)