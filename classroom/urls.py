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
    path('teacher/resetStudent/<int:student_id>/', views.resetStudent, name='resetStudent'),
    path('teacher/removeStudent/<int:student_id>/', views.removeStudent, name='removeStudent'),
    path('student/<int:classroom_id>/', views.studentClassroom, name='studentClassroom'),
    path('teacher/<int:classroom_id>/newLesson/', views.newLesson, name='newLesson'),
    path('teacher/<int:classroom_id>/editLesson/<int:lesson_id>/', views.editLesson, name='editLesson'),
    path('teacher/<int:classroom_id>/deleteLesson/<int:lesson_id>/', views.deleteLesson, name='deleteLesson'),
    path('student/<int:classroom_id>/lesson/<int:lesson_id>/', views.viewLesson, name='viewLesson'),
    path('student/<int:classroom_id>/lesson/<int:lesson_id>/survey/', views.survey, name='survey'),
    path('teacher/<int:classroom_id>/previewLesson/<int:lesson_id>/', views.previewLesson, name='previewLesson'),
]