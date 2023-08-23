from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import F, Sum

from django.core.cache import cache

from .utils import lookup
from user.decorators import allowed_users, passwordAgeCheck
from .forms import QuoteForm, BuyForm, SellForm
from .models import Transactions, Holdings
from user.models import Student

import decimal

# Create your views here.
@passwordAgeCheck()
@login_required
def index(request):
    # redirect teachers to the classroom page
    if request.user.role == 'TEACHER':
        return redirect('classroom:teacher')
    if request.method == 'POST':

        # check cache first
        if cache.get(request.user):
            student = cache.get(request.user)
        else:
            # Get the student object.
            student = get_object_or_404(Student, user=request.user)
            cache.set(request.user, student, timeout=60*60*24)
        # get the holdings of the student and group the holdings by symbol and purchase price
        holdings = Holdings.objects.filter(student=student).values('symbol', 'purchase_price').annotate(quantity=Sum('quantity'))

        
        stocks = []
        for holding in holdings:
            # check if holding is in cache
            # caching the price prevents repeat api calls, significantly improving performance
            if cache.get(holding['symbol']):
                price = cache.get(holding['symbol'])
            else:
                # Call lookup function from utils.py, the api call is made here.
                price = lookup(holding['symbol'])
                # Check if the api call was successful.
                if price == "API LIMIT":
                    messages.error(request, 'API LIMIT.')
                    return redirect('core:index')
                elif price == "INVALID SYMBOL":
                    messages.error(request, 'Invalid symbol.')
                    return redirect('core:index')
                
                # add price to cache, setting to timeout to 24 hours
                cache.set(holding['symbol'], price, timeout=60*60*24)
            
                
            
            # Calculate the total value of the stock.
            totalValue = price * decimal.Decimal(holding['quantity'])
            totalPurchasePrice = holding['purchase_price'] * (holding['quantity'])
            # Calculate the profit/loss of the stock.
            profitLoss = totalValue - totalPurchasePrice
            
            # Add the stock to the list.
            stocks.append({
                'symbol': holding['symbol'],
                'total_quantity': holding['quantity'],
                'purchase_price': holding['purchase_price'],
                'price': price,
                'totalValue': totalValue,
                'profitLoss': profitLoss,
                })
        
        # Calculate the total value of the student's portfolio.
        totalValue = sum([stock['totalValue'] for stock in stocks])

        if stocks:
            student.total_value = totalValue + student.cash
            student.save()
        return render(request, 'core/index.html', {'stocks': stocks})

    return render(request, 'core/index.html')

@login_required
@allowed_users(allowed_roles=['STUDENT'])
def buy(request):
    if request.method == 'POST':
        form = BuyForm(request.POST)
        if form.is_valid():
            symbol = form.cleaned_data['symbol'].upper()
            shares = form.cleaned_data['shares']
            
            if cache.get(symbol):
                price = cache.get(symbol)
            else:
                # Call lookup function from utils.py, the api call is made here.
                price = lookup(symbol)
                # Check if the api call was successful.
                if price == "API LIMIT":
                    messages.error(request, 'API LIMIT.')
                    return redirect('core:buy')
                elif price == "INVALID SYMBOL":
                    messages.error(request, 'Invalid symbol.')
                    return redirect('core:buy')
                
                cache.set(symbol, price, timeout=60*60*24)

            

            totalCost = price * decimal.Decimal(shares)
            
            # Get the student object.
            student = get_object_or_404(Student, user=request.user)

            # Check if the student has enough balance to make the purchase.
            if student.cash < totalCost:
                messages.error(request, 'Insufficient funds.')
                return redirect('core:buy')
            
            # Update the student's balance.
            # F is used to prevent race conditions.
            student.cash = F("cash") - totalCost
            student.save()

            # Create a transaction object.
            transaction = Transactions(student=student, symbol=symbol, quantity=shares, purchase_price=price)
            transaction.save()

            # check if the student already has a holding for this stock at this price point
            if Holdings.objects.filter(student=student, symbol=symbol, purchase_price=price).exists():
                # if so, update the holding
                holding = Holdings.objects.get(student=student, symbol=symbol, purchase_price=price)
                holding.quantity = F("quantity") + shares
                holding.save()
            else:
                holding = Holdings(student=student, symbol=symbol, purchase_price=price, quantity=shares)
                holding.save()
            
            messages.success(request, 'Successful transaction! %s %s share(s) at $%s per share.' % (shares, symbol, price))
            return render(request, 'core/index.html')

    form = BuyForm()
    return render(request, 'core/buy.html', {'form': form})

@login_required
@allowed_users(allowed_roles=['STUDENT'])
def sell(request):
    if request.method == 'POST':
        form = SellForm(request.POST, request=request)
        if form.is_valid():
            
            # Get the holding object.
            holding = form.cleaned_data['holding']
            quantity = form.cleaned_data['quantity']

            # Get the symbol of the stock.
            symbol = holding.symbol
            # Get the student object.
            student = get_object_or_404(Student, user=request.user)

            # Check if the student has enough shares to sell.
            if holding.quantity < quantity:
                messages.error(request, 'Insufficient shares.')
                return redirect('core:sell')
            
            # Update the holding object.
            if quantity == holding.quantity:
                holding.delete()
            else:
                holding.quantity = F("quantity") - quantity
                holding.save()

            if cache.get(symbol):
                price = cache.get(symbol)
            else:
                # Call lookup function from utils.py, the api call is made here.
                price = lookup(symbol)
                # Check if the api call was successful.
                if price == "API LIMIT":
                    messages.error(request, 'API LIMIT.')
                    return redirect('core:buy')
                elif price == "INVALID SYMBOL":
                    messages.error(request, 'Invalid symbol.')
                    return redirect('core:buy')
                
                cache.set(symbol, price, timeout=60*60*24)

            # calculate the profit of the sale
            profit = int((price - holding.purchase_price) * decimal.Decimal(quantity))
            # increase the students xp by 10% of the profit but cap the increase at 50
            student.xpUp(min(50, int(profit * 0.1)))
            # Update the student's balance. F is used to prevent race conditions.
            student.cash = F("cash") + (price * decimal.Decimal(quantity))
            student.save()

            # Create a transaction a new transaction for this sale.
            transaction = Transactions(student=student, symbol=symbol, quantity=-quantity, purchase_price=price)
            transaction.save()

            messages.success(request, 'Successful transaction! Sold %s %s share(s) at $%s per share. For a profit/loss of $%s!' % (quantity, symbol, price, price - holding.purchase_price))

            return render(request, 'core/index.html')
    form = SellForm(request=request)
    return render(request, 'core/sell.html', {
        'form': form
        })

@login_required
@allowed_users(allowed_roles=['STUDENT'])
def quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            symbol = form.cleaned_data['symbol'].upper()

            if cache.get(symbol):
                price = cache.get(symbol)
            else:
                # Call lookup function from utils.py, the api call is made here.
                price = lookup(symbol)
                # Check if the api call was successful.
                if price == "API LIMIT":
                    messages.error(request, 'API LIMIT.')
                    return redirect('core:quote')
                elif price == "INVALID SYMBOL":
                    messages.error(request, 'Invalid symbol.')
                    return redirect('core:quote')
                
                cache.set(symbol, price, timeout=60*60*24)

                

        symbol = symbol.upper()
        return render(request, 'core/price.html', {
        'symbol': symbol,
        'price': price
        })
    
    preSymbol = request.GET.get('symbol', '')
    form = QuoteForm()
    
    return render(request, 'core/quote.html', {
        'form': form,
        'preSymbol': preSymbol,
        })

@login_required
@allowed_users(allowed_roles=['STUDENT'])
def history(request):
    student = get_object_or_404(Student, user=request.user)
    transactions = Transactions.objects.filter(student=student)
    return render(request, 'core/history.html', {
        'transactions': transactions
        })

@login_required
@allowed_users(allowed_roles=['STUDENT'])
def leaderboard(request):
    students = Student.objects.all().order_by('-total_value')
    return render(request, 'core/leaderboard.html', {
        'students': students
        })