from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve

from .views import index, student, teacher, newClassroom, teacherClassroom, studentClassroom
from user.models import User, Student, Teacher
from .models import Classroom

# Create your tests here.
class TestUrls(SimpleTestCase):
    def test_index_url(self):
        url = reverse('classroom:index')
        self.assertEquals(resolve(url).func, index)
        
    def test_student_url(self):
        url = reverse('classroom:student')
        self.assertEquals(resolve(url).func, student)
        
    def test_teacher_url(self):
        url = reverse('classroom:teacher')
        self.assertEquals(resolve(url).func, teacher)
    
    def test_newClassroom_url(self):
        url = reverse('classroom:newClassroom')
        self.assertEquals(resolve(url).func, newClassroom)
    
    def test_teacherClassroom_url(self):
        url = reverse('classroom:teacherClassroom', args=[1])
        self.assertEquals(resolve(url).func, teacherClassroom)
    
    def test_studentClassroom_url(self):
        url = reverse('classroom:studentClassroom', args=[1])
        self.assertEquals(resolve(url).func, studentClassroom)
        
class TestIndex(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = reverse('classroom:index')
        
        self.studentUser = User.objects.create_user(username='teststudent', password='testpass', role='STUDENT')
        self.teacherUser = User.objects.create_user(username='testteacher', password='testpass', role='TEACHER')
    
    def test_index_AS_STUDENT_GET(self):
        self.client.login(username='teststudent', password='testpass')
        response = self.client.get(self.index_url)
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('classroom:student'))
    
    def test_index_AS_TEACHER_GET(self):
        self.client.login(username='testteacher', password='testpass')
        response = self.client.get(self.index_url)
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('classroom:teacher'))

class TestStudent(TestCase):
    def setUp(self):
        self.client = Client()
        self.student_url = reverse('classroom:student')
        
        self.studentUser = User.objects.create_user(username='teststudent', password='testpass', role='STUDENT')
        self.teacherUser = User.objects.create_user(username='testteacher', password='testpass', role='TEACHER')
        self.classroom = Classroom.objects.create(name='testclassroom', teacher=self.teacherUser.teacher, passcode='testpasscode')
        self.classID = Classroom.objects.get(name='testclassroom').id
    
    def test_student_GET(self):
        self.client.login(username='teststudent', password='testpass')
        response = self.client.get(self.student_url)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'classroom/student.html')
    
    def test_student_GET_as_teacher(self):
        self.client.login(username='testteacher', password='testpass')
        response = self.client.get(self.student_url)
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('classroom:teacher'))
        
    def test_student_GET_not_logged_in(self):
        response = self.client.get(self.student_url)
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('user:login') + '?next=' + self.student_url)
        
    def test_student_POST_valid_classroom(self):
        self.client.login(username='teststudent', password='testpass')
        response = self.client.post(self.student_url, {
            'name': 'testclassroom',
            'passcode': 'testpasscode'
            })
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('classroom:studentClassroom', args=[self.classID]))
        
    def test_student_POST_invalid_classroom(self):
        self.client.login(username='teststudent', password='testpass')
        response = self.client.post(self.student_url, {
            'name': 'testclassroom',
            'passcode': 'wrongpasscode'
            })
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('classroom:student'))


class TestTeacher(TestCase):
    def setUp(self):
        self.client = Client()
        self.teacher_url = reverse('classroom:teacher')
        
        self.studentUser = User.objects.create_user(username='teststudent', password='testpass', role='STUDENT')
        self.teacherUser = User.objects.create_user(username='testteacher', password='testpass', role='TEACHER')
    
    def test_teacher_GET(self):
        self.client.login(username='testteacher', password='testpass')
        response = self.client.get(self.teacher_url)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'classroom/teacher.html')
    
    def test_teacher_GET_as_student(self):
        self.client.login(username='teststudent', password='testpass')
        response = self.client.get(self.teacher_url)
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('core:index'))
    
    def test_teacher_GET_not_logged_in(self):
        response = self.client.get(self.teacher_url)
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('user:login') + '?next=' + self.teacher_url)

class TestNewClassroom(TestCase):
    def setUp(self):
        self.client = Client()
        self.newClassroom_url = reverse('classroom:newClassroom')
        
        self.studentUser = User.objects.create_user(username='teststudent', password='testpass', role='STUDENT')
        self.teacherUser = User.objects.create_user(username='testteacher', password='testpass', role='TEACHER')