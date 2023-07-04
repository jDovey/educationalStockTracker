from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve

from .views import index
# Create your tests here.

class TestUrls(SimpleTestCase):
    def test_index_url_is_resolved(self):
        url = reverse('core:index')
        self.assertEquals(resolve(url).func, index)