from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve
from django.db import transaction

from .views import index, buy, sell, quote, history, leaderboard
from .models import Holdings, Transactions
from user.models import User, Student
# Create your tests here.

class TestUrls(SimpleTestCase):
# test that the urls are resolved correctly

    def test_index_url_is_resolved(self):
        url = reverse('core:index')
        self.assertEquals(resolve(url).func, index)

    def test_buy_url_is_resolved(self):
        url = reverse('core:buy')
        self.assertEquals(resolve(url).func, buy)

    def test_sell_url_is_resolved(self):
        url = reverse('core:sell')
        self.assertEquals(resolve(url).func, sell)

    def test_quote_url_is_resolved(self):
        url = reverse('core:quote')
        self.assertEquals(resolve(url).func, quote)

    def test_history_url_is_resolved(self):
        url = reverse('core:history')
        self.assertEquals(resolve(url).func, history)

    def test_leaderboard_url_is_resolved(self):
        url = reverse('core:leaderboard')
        self.assertEquals(resolve(url).func, leaderboard)
        
class TestQuote(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = reverse('core:index')
        self.buy_url = reverse('core:buy')
        self.sell_url = reverse('core:sell')
        self.quote_url = reverse('core:quote')

        # create a user object
        self.user = User.objects.create_user(username='testuser', password='testpass', role='STUDENT')
        # login the user
        self.client.login(username='testuser', password='testpass')
    
    # test that quote view returns a 200 status code and uses the correct template on GET request with a logged in user
    def test_quote_GET(self):
        response = self.client.get(self.quote_url)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/quote.html')
    
    # test that quote view redirects to login page if user is not logged in
    def test_quote_GET_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.quote_url)
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('user:login') + '?next=' + self.quote_url)

    # test that quote view returns a 200 status code and uses the correct template on POST request with a logged in user
    def test_quote_POST(self):
        response = self.client.post(self.quote_url, {
            'symbol': 'AAPL'
            })
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/price.html')

    # test that quote view redirects back to quote page if symbol is invalid
    def test_quote_POST_invalid(self):
        response = self.client.post(self.quote_url, {
            'symbol': 'INVALID'
            })
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/quote/')

class TestIndex(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = reverse('core:index')
        self.buy_url = reverse('core:buy')
        self.sell_url = reverse('core:sell')
        self.quote_url = reverse('core:quote')

        # create a user object
        self.user = User.objects.create_user(username='testuser', password='testpass', role='STUDENT')
        # login the user
        self.client.login(username='testuser', password='testpass')
    
    # test that index view returns a 200 status code and uses the correct template on GET request with a logged in user
    def test_index_GET(self):
        response = self.client.get(self.index_url)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/index.html')
    
    # test that index view redirects to login page if user is not logged in
    def test_index_GET_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.index_url)
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('user:login') + '?next=' + self.index_url)
    
    # test that index view returns a 200 status code and uses the correct template on POST request with a logged in user
    def test_index_POST(self):
        response = self.client.post(self.index_url)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/index.html')

class TestBuy(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = reverse('core:index')
        self.buy_url = reverse('core:buy')
        self.sell_url = reverse('core:sell')
        self.quote_url = reverse('core:quote')

        # create a user object
        self.user = User.objects.create_user(username='testuser', password='testpass', role='STUDENT')
        # login the user
        self.client.login(username='testuser', password='testpass')
    
    # test that buy view returns a 200 status code and uses the correct template on GET request with a logged in user
    def test_buy_GET(self):
        response = self.client.get(self.buy_url)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/buy.html')
    
    # test that buy view redirects to login page if user is not logged in
    def test_buy_GET_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.buy_url)
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('user:login') + '?next=' + self.buy_url)

    # test that buy view returns a 200 status code and uses the correct template on POST request with a logged in user
    def test_buy_POST(self):
        with transaction.atomic():
            response = self.client.post(self.buy_url, {
                'symbol': 'AAPL',
                'shares': 1
                })
        
        self.user.student.refresh_from_db()
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/index.html')
        self.assertEquals(Holdings.objects.count(), 1)
        self.assertEquals(Transactions.objects.count(), 1)
        # test that the student's cash is updated
        self.assertNotEquals(self.user.student.cash, 10000)
    
    # test that buy view redirects back to buy page if symbol is invalid
    def test_buy_POST_invalid_symbol(self):
        response = self.client.post(self.buy_url, {
            'symbol': 'INVALID',
            'shares': 1
            })
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/buy/')

    # test that buy view redirects back to buy page if not enough cash
    def test_buy_POST_not_enough_cash(self):
        response = self.client.post(self.buy_url, {
            'symbol': 'AAPL',
            'shares': 1000000000
            })
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/buy/')

class TestSell(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = reverse('core:index')
        self.sell_url = reverse('core:sell')

        # create a user object
        self.user = User.objects.create_user(username='testuser', password='testpass', role='STUDENT')
        # login the user
        self.client.login(username='testuser', password='testpass')

        # create a holding object
        self.holding = Holdings.objects.create(student=self.user.student, symbol='AAPL', quantity=1, purchase_price=1.00, )
        
    # test that sell view returns a 200 status code and uses the correct template on GET request with a logged in user
    def test_sell_GET(self):
        response = self.client.get(self.sell_url)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/sell.html')
    
    # test that sell view redirects to login page if user is not logged in
    def test_sell_GET_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.sell_url)
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('user:login') + '?next=' + self.sell_url)
    
    # test that sell view returns a 200 status code and uses the correct template on POST request with a logged in user
    # and valid shares
    def test_sell_POST(self):
        response = self.client.post(self.sell_url, {
            # pass in holding object pk as the form uses a model choice field
            'holding': self.holding.pk,
            'quantity': 1
            })
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/index.html')
        # check that holding object has been deleted
        self.assertEquals(Holdings.objects.count(), 0)
        # check that transaction object has been created
        self.assertEquals(Transactions.objects.count(), 1)
    
    def test_sell_POST_invalid_shares(self):
        response = self.client.post(self.sell_url, {
            # pass in holding object pk as the form uses a model choice field
            'holding': self.holding.pk,
            'quantity': 200
            })
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/sell/')
        # check that holding object has not been deleted
        self.assertEquals(Holdings.objects.count(), 1)
        self.assertEquals(Transactions.objects.count(), 0)

class TestHistory(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = reverse('core:index')
        self.history_url = reverse('core:history')

        # create a user object
        self.user = User.objects.create_user(username='testuser', password='testpass', role='STUDENT')
        # login the user
        self.client.login(username='testuser', password='testpass')

        # create a holding object
        self.holding = Holdings.objects.create(student=self.user.student, symbol='AAPL', quantity=1, purchase_price=1.00, )
        # create a transaction object
        self.transaction = Transactions.objects.create(student=self.user.student, symbol='AAPL', quantity=1, purchase_price=1.00)
    
    # test that history view returns a 200 status code and uses the correct template on GET request with a logged in user
    def test_history_GET(self):
        response = self.client.get(self.history_url)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/history.html')
    
    # test that history view redirects to login page if user is not logged in
    def test_history_GET_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.history_url)
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('user:login') + '?next=' + self.history_url)

class TestLeaderboard(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = reverse('core:index')
        self.leaderboard_url = reverse('core:leaderboard')

        # create a user object
        self.user = User.objects.create_user(username='testuser', password='testpass', role='STUDENT')
        # login the user
        self.client.login(username='testuser', password='testpass')

        # create a holding object
        self.holding = Holdings.objects.create(student=self.user.student, symbol='AAPL', quantity=1, purchase_price=1.00, )
        # create a transaction object
        self.transaction = Transactions.objects.create(student=self.user.student, symbol='AAPL', quantity=1, purchase_price=1.00)
    
    # test that leaderboard view returns a 200 status code and uses the correct template on GET request with a logged in user
    def test_leaderboard_GET(self):
        response = self.client.get(self.leaderboard_url)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/leaderboard.html')
    
    # test that leaderboard view redirects to login page if user is not logged in
    def test_leaderboard_GET_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.leaderboard_url)
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('user:login') + '?next=' + self.leaderboard_url)

class TestHoldingsModel(TestCase):
    def setUp(self):
        # create a user object
        self.user = User.objects.create_user(username='testuser', password='testpass', role='STUDENT')
        # create a holding object
        self.holding = Holdings.objects.create(student=self.user.student, symbol='AAPL', quantity=1, purchase_price=1.00, )
    
    # test that holding object is created correctly
    def test_holding_creation(self):
        self.assertEquals(self.holding.student, self.user.student)
        self.assertEquals(self.holding.symbol, 'AAPL')
        self.assertEquals(self.holding.quantity, 1)
        self.assertEquals(self.holding.purchase_price, 1.00)
    
    # test that holding object is deleted correctly
    def test_holding_deletion(self):
        self.holding.delete()
        self.assertEquals(Holdings.objects.count(), 0)

class TestTransactionsModel(TestCase):
    def setUp(self):
        # create a user object
        self.user = User.objects.create_user(username='testuser', password='testpass', role='STUDENT')
        # create a transaction object
        self.transaction = Transactions.objects.create(student=self.user.student, symbol='AAPL', quantity=1, purchase_price=1.00)
    
    # test that transaction object is created correctly
    def test_transaction_creation(self):
        self.assertEquals(self.transaction.student, self.user.student)
        self.assertEquals(self.transaction.symbol, 'AAPL')
        self.assertEquals(self.transaction.quantity, 1)
        self.assertEquals(self.transaction.purchase_price, 1.00)
    
    # test that transaction object is deleted correctly
    def test_transaction_deletion(self):
        self.transaction.delete()
        self.assertEquals(Transactions.objects.count(), 0)
