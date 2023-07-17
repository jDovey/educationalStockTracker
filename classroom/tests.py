from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve

from .views import index, student, teacher, newClassroom, teacherClassroom, studentClassroom

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