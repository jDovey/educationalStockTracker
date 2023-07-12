from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from user.models import Student
from .models import Classroom
from user.decorators import allowed_users
from .forms import NewClassroomForm

# Create your views here.

@login_required
def index(request):
    if request.user.role == 'STUDENT':
        return redirect('classroom:student')
    elif request.user.role == 'TEACHER':
        return redirect('classroom:teacher')
    return render(request, 'classroom/index.html')

@login_required
@allowed_users(allowed_roles=['STUDENT'])
def student(request):
    return render(request, 'classroom/student.html')

@login_required
@allowed_users(allowed_roles=['TEACHER'])
def teacher(request):
    # get the classrooms of the teacher
    teacher_classrooms = Classroom.objects.filter(teacher=request.user.teacher)
    return render(request, 'classroom/teacher.html', {'teacher_classrooms': teacher_classrooms})

@login_required
@allowed_users(allowed_roles=['TEACHER'])
def newClassroom(request):
    if request.method == 'POST':
        form = NewClassroomForm(request.POST)
        if form.is_valid():
            classroom = form.save(commit=False)
            classroom.teacher = request.user.teacher
            classroom.save()
            
            return redirect('classroom:teacher')
    form = NewClassroomForm()
    return render(request, 'classroom/newClassroom.html', {
        'form': form,
        })

@login_required
@allowed_users(allowed_roles=['TEACHER'])
def teacherClassroom(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    if classroom.teacher != request.user.teacher:
        messages.error(request, 'You do not have permission to view this classroom.')
        return redirect('classroom:teacher')
    classroomStudents = Student.objects.filter(classroom=classroom)
    return render(request, 'classroom/teacherClassroom.html', {
        'classroom': classroom,
        'classroomStudents': classroomStudents,
        })