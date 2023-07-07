from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve

from .views import index, buy, sell, quote
# Create your tests here.

class TestUrls(SimpleTestCase):

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