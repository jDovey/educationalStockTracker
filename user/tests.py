from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve

from .views import register, login, logout

from .models import User, Student
# Create your tests here.

class TestUrls(SimpleTestCase):

    def test_register_url_is_resolved(self):
        url = reverse('user:register')
        self.assertEquals(resolve(url).func, register)

    def test_login_url_is_resolved(self):
        url = reverse('user:login')
        self.assertEquals(resolve(url).func, login)

    def test_logout_url_is_resolved(self):
        url = reverse('user:logout')
        self.assertEquals(resolve(url).func, logout)



    