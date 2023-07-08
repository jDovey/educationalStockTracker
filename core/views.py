from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import F, Count

from .utils import lookup
from user.decorators import allowed_users
from .forms import QuoteForm, BuyForm, SellForm
from .models import Transactions, Holdings
from user.models import Student

import decimal

# Create your views here.
@login_required
@allowed_users(allowed_roles=['STUDENT'])
def index(request):
    if request.method == 'POST':
        # Get the student object.
        student = get_object_or_404(Student, user=request.user)
        # Get the holdings of the student.
        holdings = Holdings.objects.filter(student=student).values('symbol').annotate(total_quantity=Count('symbol'), total_purchase_price=F('purchase_price') * F('total_quantity')).order_by('symbol')
        
        stocks = []
        for holding in holdings:
            # Call lookup function from utils.py, the api call is made here.
            price = lookup(holding['symbol'])
            
            # Check if the api call was successful.
            if price == "API LIMIT":
                messages.error(request, 'API LIMIT.')
                return redirect('core:history')
            elif price == "INVALID SYMBOL":
                messages.error(request, 'Invalid symbol.')
                return redirect('core:history')
            
            # Calculate the total value of the stock.
            totalValue = price * decimal.Decimal(holding['total_quantity'])
            
            # Calculate the profit/loss of the stock.
            profitLoss = totalValue - decimal.Decimal(holding['total_purchase_price'])
            
            # Add the stock to the list.
            stocks.append({
                'symbol': holding['symbol'],
                'total_quantity': holding['total_quantity'],
                'total_purchase_price': holding['total_purchase_price'],
                'price': price,
                'totalValue': totalValue,
                'profitLoss': profitLoss,
                })
        return render(request, 'core/index.html', {'stocks': stocks, 'balance': student.balance})

    return render(request, 'core/index.html')

@login_required
@allowed_users(allowed_roles=['STUDENT'])
def buy(request):
    if request.method == 'POST':
        form = BuyForm(request.POST)
        if form.is_valid():
            symbol = form.cleaned_data['symbol']
            shares = form.cleaned_data['shares']

            # Call lookup function from utils.py, the api call is made here.
            price = lookup(symbol)

            # Check if the api call was successful.
            if price == "API LIMIT":
                messages.error(request, 'API LIMIT.')
                return redirect('core:buy')
            elif price == "INVALID SYMBOL":
                messages.error(request, 'Invalid symbol.')
                return redirect('core:buy')

            totalCost = price * decimal.Decimal(shares)
            
            # Get the student object.
            student = get_object_or_404(Student, user=request.user)

            # Check if the student has enough balance to make the purchase.
            if student.balance < totalCost:
                messages.error(request, 'Insufficient funds.')
                return redirect('core:buy')
            
            # Update the student's balance.
            # F is used to prevent race conditions.
            student.balance = F("balance") - totalCost
            student.save()
            transaction = Transactions(student=student, symbol=symbol, quantity=shares, purchase_price=price)
            transaction.save()

            for i in range(shares):
                holding = Holdings(student=student, symbol=symbol, purchase_price=price)
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
            # Get the symbol of the stock.
            symbol = holding.symbol
            # Get the price of the stock.
            price = lookup(symbol)
            # Get the student object.
            student = get_object_or_404(Student, user=request.user)
            # Update the student's balance. F is used to prevent race conditions.
            student.balance = F("balance") + price
            student.save()
            holding.delete()
            # Create a transaction a new transaction for this sale.
            transaction = Transactions(student=student, symbol=symbol, quantity=-1, purchase_price=price)
            transaction.save()
            messages.success(request, 'Successful transaction! Sold 1 %s share at $%s per share. For a profit/loss of $%s!' % (symbol, price, price - holding.purchase_price))
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
            symbol = form.cleaned_data['symbol']
            print(symbol)

            price = lookup(symbol)

            # Check if the api call was successful.
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

@login_required
@allowed_users(allowed_roles=['STUDENT'])
def history(request):
    student = get_object_or_404(Student, user=request.user)
    transactions = Transactions.objects.filter(student=student)
    return render(request, 'core/history.html', {
        'transactions': transactions
        })