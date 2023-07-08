from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .utils import lookup
from user.decorators import allowed_users
from .forms import QuoteForm

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
    if request.method == 'POST':
        symbol = request.POST['symbol']

        price = lookup(symbol)

        if price == "API LIMIT":
            messages.error(request, 'API LIMIT.')
            return redirect('core:quote')
        elif price == "INVALID SYMBOL":
            messages.error(request, 'Invalid symbol.')
            return redirect('core:quote')

        symbol = symbol.upper()
        return render(request, 'core/price.html', {
        'symbol': symbol,
        'price': price
        })
    
        
        
    
    form = QuoteForm()
    return render(request, 'core/quote.html', {'form': form})