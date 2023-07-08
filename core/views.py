from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .utils import lookup
from user.decorators import allowed_users

# Create your views here.
def index(request):
    return render(request, 'core/index.html')

@login_required
@allowed_users(allowed_roles=['STUDENT'])
def buy(request):
    lookup('AAPL')
    return render(request, 'core/buy.html')

@login_required
@allowed_users(allowed_roles=['STUDENT'])
def sell(request):
    return render(request, 'core/sell.html')

@login_required
@allowed_users(allowed_roles=['STUDENT'])
def quote(request):
    return render(request, 'core/quote.html')