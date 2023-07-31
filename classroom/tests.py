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
    
    # test that the index page redirects to the correct page based on the user's role
    def test_index_AS_STUDENT_GET(self):
        self.client.login(username='teststudent', password='testpass')
        response = self.client.get(self.index_url)
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('classroom:student'))
    
    # test that the index page redirects to the correct page based on the user's role
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
    
    # test that a student without a classroom will go to the student page
    def test_student_GET(self):
        self.client.login(username='teststudent', password='testpass')
        response = self.client.get(self.student_url)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'classroom/student.html')
    
    # test that a student with a classroom will go to the classroom page
    def test_student_GET_with_classroom(self):
        # add the classroom to the student
        self.studentUser.student.classroom = self.classroom
        self.studentUser.student.save()
        
        self.client.login(username='teststudent', password='testpass')
        response = self.client.get(self.student_url)
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('classroom:studentClassroom', args=[self.classID]))
    
    # test that a teacher will be redirected to the teacher page
    def test_student_GET_as_teacher(self):
        self.client.login(username='testteacher', password='testpass')
        response = self.client.get(self.student_url)
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('classroom:teacher'))
    
    # test that a user who is not logged in will be redirected to the login page
    def test_student_GET_not_logged_in(self):
        response = self.client.get(self.student_url)
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('user:login') + '?next=' + self.student_url)
    
    # test that a student can join a valid classroom with the correct passcode
    def test_student_POST_valid_classroom(self):
        self.client.login(username='teststudent', password='testpass')
        response = self.client.post(self.student_url, {
            'name': 'testclassroom',
            'passcode': 'testpasscode'
            })
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('classroom:studentClassroom', args=[self.classID]))
    
    # test that a student cannot join a valid classroom with the incorrect passcode
    def test_student_POST_invalid_passcode(self):
        self.client.login(username='teststudent', password='testpass')
        response = self.client.post(self.student_url, {
            'name': 'testclassroom',
            'passcode': 'wrongpasscode'
            })
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('classroom:student'))
    
    # test that a student cannot join an invalid classroom
    def test_student_POST_invalid_classroom(self):
        self.client.login(username='teststudent', password='testpass')
        response = self.client.post(self.student_url, {
            'name': 'wrongclassroom',
            'passcode': 'testpasscode'
            })
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('classroom:student'))


class TestTeacher(TestCase):
    def setUp(self):
        self.client = Client()
        self.teacher_url = reverse('classroom:teacher')
        
        self.studentUser = User.objects.create_user(username='teststudent', password='testpass', role='STUDENT')
        self.teacherUser = User.objects.create_user(username='testteacher', password='testpass', role='TEACHER')
    
    # test that a teacher will go to the teacher page
    def test_teacher_GET(self):
        self.client.login(username='testteacher', password='testpass')
        response = self.client.get(self.teacher_url)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'classroom/teacher.html')
    
    # test that a student will be redirected to the student page
    def test_teacher_GET_as_student(self):
        self.client.login(username='teststudent', password='testpass')
        response = self.client.get(self.teacher_url)
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('core:index'))
    
    # test that a user who is not logged in will be redirected to the login page
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
    
    # test that the correct template is used when the page is loaded
    def test_newClassroom_GET(self):
        self.client.login(username='testteacher', password='testpass')
        response = self.client.get(self.newClassroom_url)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'classroom/newClassroom.html')
    
    # test that a student will be redirected to the student page
    def test_newClassroom_GET_as_student(self):
        self.client.login(username='teststudent', password='testpass')
        response = self.client.get(self.newClassroom_url)
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('core:index'))
        
    # test that a user who is not logged in will be redirected to the login page
    def test_newClassroom_GET_not_logged_in(self):
        response = self.client.get(self.newClassroom_url)
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('user:login') + '?next=' + self.newClassroom_url)
        
    # test that the view returns a 200 status code when a teacher creates a new classroom
    def test_newClassroom_POST(self):
        self.client.login(username='testteacher', password='testpass')
        response = self.client.post(self.newClassroom_url, {
            'name': 'testclassroom',
            'passcode': 'testpasscode'
            })
        
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Classroom.objects.count(), 1)
        self.assertRedirects(response, reverse('classroom:teacherClassroom', args=[1]))
        
    # test that the view does not allow duplicate classroom names
    def test_newClassroom_POST_duplicate_name(self):
        self.client.login(username='testteacher', password='testpass')
        response = self.client.post(self.newClassroom_url, {
            'name': 'testclassroom',
            'passcode': 'testpasscode'
            })
        response = self.client.post(self.newClassroom_url, {
            'name': 'testclassroom',
            'passcode': 'testpasscode'
            })
        
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Classroom.objects.count(), 1)
        self.assertTemplateUsed(response, 'classroom/newClassroom.html')
    
class TestTeacherClassroom(TestCase):
    def setUp(self):
        self.client = Client()
        
        self.studentUser = User.objects.create_user(username='teststudent', password='testpass', role='STUDENT')
        self.teacherUser = User.objects.create_user(username='testteacher', password='testpass', role='TEACHER')
        
        self.classroom = Classroom.objects.create(name='testclassroom', teacher=self.teacherUser.teacher, passcode='testpasscode')
        self.teacherClassroom_url = reverse('classroom:teacherClassroom', args=[self.classroom.id])
        
    # test that the correct template is used when the page is loaded
    def test_teacherClassroom_GET(self):
        self.client.login(username='testteacher', password='testpass')
        response = self.client.get(self.teacherClassroom_url)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'classroom/teacherClassroom.html')
    
    # test that a student will be redirected to the student page
    def test_teacherClassroom_GET_as_student(self):
        self.client.login(username='teststudent', password='testpass')
        response = self.client.get(self.teacherClassroom_url)
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('core:index'))
    
    # test that a user who is not logged in will be redirected to the login page
    def test_teacherClassroom_GET_not_logged_in(self):
        response = self.client.get(self.teacherClassroom_url)
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('user:login') + '?next=' + self.teacherClassroom_url)
    
    # test that a teacher cannot access a classroom that they do not own
    def test_teacherClassroom_GET_not_owner(self):
        # create a new teacher
        User.objects.create_user(username='testteacher2', password='testpass', role='TEACHER').teacher
        
        # login as the new teacher
        self.client.login(username='testteacher2', password='testpass')
        response = self.client.get(self.teacherClassroom_url)
        
        # teacher should be redirected to the teacher page as they do not own the classroom
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('classroom:teacher'))
        
class TestStudentClassroom(TestCase):
    def setUp(self):
        self.client = Client()
        self.teacherUser = User.objects.create_user(username='testteacher', password='testpass', role='TEACHER')
        self.classroom = Classroom.objects.create(name='testclassroom', teacher=self.teacherUser.teacher, passcode='testpasscode')
        self.studentUser = User.objects.create_user(username='teststudent', password='testpass', role='STUDENT')
        self.studentClassroom_url = reverse('classroom:studentClassroom', args=[self.classroom.id])
        
    # test that the correct template is used when the page is loaded
    def test_studentClassroom_GET(self):
        # add the classroom to the student
        self.studentUser.student.classroom = self.classroom
        self.studentUser.student.save()
        
        self.client.login(username='teststudent', password='testpass')
        response = self.client.get(self.studentClassroom_url)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'classroom/studentClassroom.html')
    
    # test that a teacher will be redirected to the teacher page
    def test_studentClassroom_GET_as_teacher(self):
        self.client.login(username='testteacher', password='testpass')
        response = self.client.get(self.studentClassroom_url)
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('classroom:teacher'))
    
    # test that a user who is not logged in will be redirected to the login page
    def test_studentClassroom_GET_not_logged_in(self):
        response = self.client.get(self.studentClassroom_url)
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('user:login') + '?next=' + self.studentClassroom_url)
        
    # test that a student cannot access a classroom that they do not belong to
    def test_studentClassroom_GET_not_in_classroom(self):
        # create a new student
        User.objects.create_user(username='teststudent2', password='testpass', role='STUDENT').student
        
        # login as the new student
        self.client.login(username='teststudent2', password='testpass')
        response = self.client.get(self.studentClassroom_url)
        
        # student should be redirected to the student page as they do not belong to the classroom
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('classroom:student'))