from django.urls import path

from . import views

app_name = 'classroom'

urlpatterns = [
    path('', views.index, name='index'),
    path('student/', views.student, name='student'),
    path('teacher/', views.teacher, name='teacher'),
    path('teacher/newClassroom/', views.newClassroom, name='newClassroom'),
    path('teacher/<int:classroom_id>/', views.teacherClassroom, name='teacherClassroom')
]