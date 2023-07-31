from django.urls import path

from . import views

app_name = 'classroom'

urlpatterns = [
    path('', views.index, name='index'),
    path('student/', views.student, name='student'),
    path('teacher/', views.teacher, name='teacher'),
    path('teacher/newClassroom/', views.newClassroom, name='newClassroom'),
    path('teacher/<int:classroom_id>/', views.teacherClassroom, name='teacherClassroom'),
    path('teacher/editStudent/<int:student_id>/', views.editStudent, name='editStudent'),
    path('teacher/removeStudent/<int:student_id>/', views.removeStudent, name='removeStudent'),
    path('student/<int:classroom_id>/', views.studentClassroom, name='studentClassroom'),
    path('teacher/<int:classroom_id>/newLesson/', views.newLesson, name='newLesson'),
]