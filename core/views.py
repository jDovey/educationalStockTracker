from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .utils import lookup

# Create your views here.


def index(request):
    return render(request, 'core/index.html')

@login_required
def buy(request):
    lookup('AAPL')
    return render(request, 'core/buy.html')

@login_required
def sell(request):
    return render(request, 'core/sell.html')

@login_required
def quote(request):
    return render(request, 'core/quote.html')