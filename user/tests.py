from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth import views as auth_views

from .views import register

from .models import User, Student
# Create your tests here.

class TestUrls(SimpleTestCase):
    # test that the urls are resolved correctly
    
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
        self.validUser = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'role': 'STUDENT'
        }
        self.invalidUser = {
            'username': 'testuser',
            'email': 'nonemail',
            'password1': 'testpassword',
            'password2': 'nonmatchingpassword',
            'role': 'STUDENT'
        }

    # test that register view returns a 200 status code and uses the correct template on GET request
    def test_register_GET(self):
        response = self.client.get(self.register_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/register.html')

    # test that register view returns a 302 status code and redirects to the index page on POST request
    def test_register_POST(self):
        # post the user to the register url
        response = self.client.post(self.register_url, self.validUser)
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

    # test that register view returns a 200 status code and uses the correct template on POST request with invalid data
    def test_register_POST_invalid(self):        
        # post the user to the register url
        response = self.client.post(self.register_url, self.invalidUser)
        # check that the user is redirected
        self.assertEquals(response.status_code, 200)
        # check that the user is not created
        self.assertEquals(User.objects.count(), 0)
        # check that the student is not created
        self.assertEquals(Student.objects.count(), 0)

class TestUserModel(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='testuserStudent',
            email='test@test.com',
            password='testpassword',
            role='STUDENT'
        )
    
    # test that a user is created and that the user's attributes are correct
    def test_user_is_created(self):
        self.assertEquals(User.objects.count(), 1)
        self.assertEquals(User.objects.get().username, 'testuserStudent')
        self.assertEquals(User.objects.get().email, 'test@test.com')
        self.assertEquals(User.objects.get().role, 'STUDENT')

    # test that a user is deleted correctly
    def test_user_is_deleted(self):
        self.user.delete()
        self.assertEquals(User.objects.count(), 0)

class TestStudentModel(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='testuserStudent',
            email='test@test.com',
            password='testpassword',
            role='STUDENT'
        )
    
    # test that a student is created and that the student's attributes are correct
    def test_student_is_created(self):
        self.assertEquals(Student.objects.count(), 1)
        self.assertEquals(Student.objects.get().user.username, 'testuserStudent')
        self.assertEquals(Student.objects.get().user.email, 'test@test.com')
        self.assertEquals(Student.objects.get().user.role, 'STUDENT')
    
    # test that a student is deleted correctly when its user is deleted
    def test_student_is_deleted(self):
        self.user.delete()
        self.assertEquals(Student.objects.count(), 0)

class TestTeacherModel(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='testuserTeacher',
            email='test@test.com',
            password='testpassword',
            role='TEACHER'
        )
    
    # test that a teacher is created and that the teacher's attributes are correct
    def test_teacher_is_created(self):
        self.assertEquals(User.objects.count(), 1)
        self.assertEquals(User.objects.get().username, 'testuserTeacher')
        self.assertEquals(User.objects.get().email, 'test@test.com')
        self.assertEquals(User.objects.get().role, 'TEACHER')
    
    # test that a teacher is deleted correctly when its user is deleted
    def test_teacher_is_deleted(self):
        self.user.delete()
        self.assertEquals(User.objects.count(), 0)