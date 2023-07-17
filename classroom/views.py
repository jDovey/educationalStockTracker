from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from user.models import Student
from .models import Classroom
from user.decorators import allowed_users
from .forms import NewClassroomForm, JoinClassroomForm

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
    if request.user.student.classroom:
        return redirect('classroom:studentClassroom', classroom_id=request.user.student.classroom.id)
    if request.method == 'POST':
        form = JoinClassroomForm(request.POST)
        if form.is_valid():
            classroom = Classroom.objects.get(name=form.cleaned_data['name'])
            passcode = form.cleaned_data['passcode']
            
            print(passcode, classroom.passcode)
            if classroom.passcode == passcode:
                student = request.user.student
                student.classroom = classroom
                student.save()
                successMessage = "You have successfully joined %s's classroom." % classroom.teacher.user.username
                messages.success(request, 'You have successfully joined the classroom.')
                
                return redirect('classroom:studentClassroom', classroom_id=classroom.id)
    form = JoinClassroomForm()
    return render(request, 'classroom/student.html', {
        'form': form
        })

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
            # save the classroom without committing to the database
            classroom = form.save(commit=False)
            # this allows us to add the teacher to the classroom
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
    
@login_required
@allowed_users(allowed_roles=['STUDENT'])
def studentClassroom(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    # get the students in the classroom order by their total_value
    classroomStudents = Student.objects.filter(classroom=classroom).order_by('-total_value')
    return render(request, 'classroom/studentClassroom.html', {
        'classroom': classroom,
        'classroomStudents': classroomStudents,
        })