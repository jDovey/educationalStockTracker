from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth import views as auth_views

from .views import register

from .models import User, Student
# Create your tests here.

class TestUrls(SimpleTestCase):

    def test_register_url_is_resolved(self):
        url = reverse('user:register')
        self.assertEquals(resolve(url).func, register)

    def test_login_url_is_resolved(self):
        url = reverse('user:login')
        self.assertEquals(resolve(url).func.view_class, auth_views.LoginView)

    def test_logout_url_is_resolved(self):
        url = reverse('user:logout')
        self.assertEquals(resolve(url).func.view_class, auth_views.LogoutView)

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('user:register')

    # test that register view returns a 200 status code and uses the correct template on GET request
    def test_register_GET(self):
        client = Client()
        response = client.get(reverse('user:register'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/register.html')

    def test_register_POST(self):
        # create a user
        user = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'role': 'STUDENT'
        }

        # post the user to the register url
        response = self.client.post(self.register_url, user)
        # check that the user is redirected to the index page
        self.assertEquals(response.status_code, 302)
        # check that the user is created
        self.assertEquals(User.objects.count(), 1)
        # check that the student is created
        self.assertEquals(Student.objects.count(), 1)
        # check that the student's user is the user we created
        self.assertEquals(Student.objects.get().user.username, 'testuser')
        # check that the user is logged in
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_register_POST_invalid(self):
        # create a user
        user = {
            'username': 'testuser',
            'email': 'nonemail',
            'password1': 'testpassword',
            'password2': 'nonmatchingpassword',
            'role': 'STUDENT'
        }

        # post the user to the register url
        response = self.client.post(self.register_url, user)
        # check that the user is redirected
        self.assertEquals(response.status_code, 200)
        # check that the user is not created
        self.assertEquals(User.objects.count(), 0)
        # check that the student is not created
        self.assertEquals(Student.objects.count(), 0)

class TestModels(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            email='test@test.com',
            password='testpassword',
            role='STUDENT'
        )
        
        
