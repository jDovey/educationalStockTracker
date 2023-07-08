from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve

from .views import index, buy, sell, quote
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
        
class TestViews(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.index_url = reverse('core:index')
        self.buy_url = reverse('core:buy')
        self.sell_url = reverse('core:sell')
        self.quote_url = reverse('core:quote')
        self.student = {
            'username': 'student',
            'email': 'test@test.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'role': 'STUDENT'
        }
        self.teacher = {
            'username': 'teacher',
            'email': 'test@test.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'role': 'TEACHER'
        }
        
    # test that index view returns a 200 status code and uses the correct template on GET request
    def test_index_GET(self):
        response = self.client.get(self.index_url)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/index.html')
    
    # test that buy view returns a 200 status code and uses the correct template on GET request
    def test_buy_GET(self):
        response = self.client.get(self.buy_url)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/buy.html')
        
    # test that sell view returns a 200 status code and uses the correct template on GET request
    def test_sell_GET(self):
        response = self.client.get(self.sell_url)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/sell.html')
    
    # test that quote view returns a 200 status code and uses the correct template on GET request
    def test_quote_GET(self):
        response = self.client.get(self.quote_url)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/quote.html')
        