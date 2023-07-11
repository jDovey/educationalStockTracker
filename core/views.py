from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import F, Sum

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
        # get the holdings of the student and group the holdings by symbol and purchase price
        holdings = Holdings.objects.filter(student=student).values('symbol', 'purchase_price').annotate(quantity=Sum('quantity'))

        
        stocks = []
        prices = {}
        for holding in holdings:
            # Call lookup function from utils.py, the api call is made here.
            if holding['symbol'] not in prices:
                price = lookup(holding['symbol'])
                prices[holding['symbol']] = price
            
            # Check if the api call was successful.
            if prices[holding['symbol']] == "API LIMIT":
                messages.error(request, 'API LIMIT.')
                return redirect('core:history')
            elif prices[holding['symbol']] == "INVALID SYMBOL":
                messages.error(request, 'Invalid symbol.')
                return redirect('core:history')
            
            # Calculate the total value of the stock.
            totalValue = prices[holding['symbol']] * decimal.Decimal(holding['quantity'])
            totalPurchasePrice = holding['purchase_price'] * (holding['quantity'])
            # Calculate the profit/loss of the stock.
            profitLoss = totalValue - totalPurchasePrice
            
            # Add the stock to the list.
            stocks.append({
                'symbol': holding['symbol'],
                'total_quantity': holding['quantity'],
                'purchase_price': holding['purchase_price'],
                'price': prices[holding['symbol']],
                'totalValue': totalValue,
                'profitLoss': profitLoss,
                })
        
        if stocks:
            student.total_value = totalValue + F('cash')
            student.save()
        return render(request, 'core/index.html', {'stocks': stocks})

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

            # Get the price of the stock.
            price = lookup(symbol)

            # Check if the api call was successful.
            if price == "API LIMIT":
                messages.error(request, 'API LIMIT.')
                return redirect('core:sell')
            elif price == "INVALID SYMBOL":
                messages.error(request, 'Invalid symbol.')
                return redirect('core:sell')

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

@login_required
@allowed_users(allowed_roles=['STUDENT'])
def leaderboard(request):
    students = Student.objects.all().order_by('-total_value')
    return render(request, 'core/leaderboard.html', {
        'students': students
        })