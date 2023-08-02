from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from user.models import Student
from .models import Classroom, Lesson
from user.decorators import allowed_users
from .forms import NewClassroomForm, JoinClassroomForm, EditStudentForm, LessonForm

# Create your views here.

@login_required
@allowed_users(allowed_roles=['STUDENT', 'TEACHER'])
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
            
            try:
                classroom = Classroom.objects.get(name=form.cleaned_data['name'])
            except Classroom.DoesNotExist:
                messages.error(request, 'The classroom you entered does not exist.')
                return redirect('classroom:student')
            
            passcode = form.cleaned_data['passcode']
            if classroom.passcode == passcode:
                student = request.user.student
                student.classroom = classroom
                student.save()
                successMessage = "You have successfully joined %s's classroom." % classroom.teacher.user.username
                messages.success(request, successMessage)
                
                return redirect('classroom:studentClassroom', classroom_id=classroom.id)
            else:
                messages.error(request, 'The passcode you entered is incorrect.')
                return redirect('classroom:student')
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
            
            return redirect('classroom:teacherClassroom', classroom_id=classroom.id)
        else:
            return render(request, 'classroom/newClassroom.html', {
                'form': form,
            })
            
    form = NewClassroomForm()
    return render(request, 'classroom/newClassroom.html', {
        'form': form,
        })

@login_required
@allowed_users(allowed_roles=['TEACHER'])
def teacherClassroom(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    # check if the classroom belongs to the teacher
    if classroom.teacher != request.user.teacher:
        messages.error(request, 'You do not have permission to view this classroom.')
        return redirect('classroom:teacher')
    classroomStudents = Student.objects.filter(classroom=classroom).order_by('-total_value')
    # get the lessons in the classroom order by their order
    classroomLessons = Lesson.objects.filter(classroom=classroom).order_by('order')
    return render(request, 'classroom/teacherClassroom.html', {
        'classroom': classroom,
        'classroomStudents': classroomStudents,
        'classroomLessons': classroomLessons,
        })
    
@login_required
@allowed_users(allowed_roles=['STUDENT'])
def studentClassroom(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    # check if the classroom belongs to the student
    if classroom != request.user.student.classroom:
        messages.error(request, 'You do not have permission to view this classroom.')
        return redirect('classroom:student')
    # get the students in the classroom order by their total_value
    classroomStudents = Student.objects.filter(classroom=classroom).order_by('-total_value')
    # get the published lessons in the classroom order by their order
    classroomLessons = Lesson.objects.filter(classroom=classroom, status='PUBLISHED').order_by('order')
    return render(request, 'classroom/studentClassroom.html', {
        'classroom': classroom,
        'classroomStudents': classroomStudents,
        'classroomLessons': classroomLessons,
        })
    
@login_required
@allowed_users(allowed_roles=['TEACHER'])
def editStudent(request, student_id):
    student = Student.objects.get(user_id=student_id)
    if student.classroom.teacher != request.user.teacher:
        messages.error(request, 'You do not have permission to edit this student.')
        return redirect('classroom:teacher')
    
    if request.method == 'POST':
        form = EditStudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('classroom:teacherClassroom', classroom_id=student.classroom.id)
    form = EditStudentForm(instance=student)
    return render(request, 'classroom/editStudent.html', {
        'form': form,
        'student': student,
        })

@login_required
@allowed_users(allowed_roles=['TEACHER'])
def removeStudent(request, student_id):
    student = Student.objects.get(user_id=student_id)
    classroom_id = student.classroom.id
    if student.classroom.teacher != request.user.teacher:
        messages.error(request, 'You do not have permission to remove this student.')
        return redirect('classroom:teacher')
    
    
    student.classroom = None
    student.save()
    messages.success(request, 'You have successfully removed %s from your classroom.' % student.user.username)
    return redirect('classroom:teacherClassroom', classroom_id)
    
@login_required
@allowed_users(allowed_roles=['TEACHER'])
def newLesson(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            # check if the order and classroom combination already exists
            if Lesson.objects.filter(order=form.cleaned_data['order'], classroom=Classroom.objects.get(id=classroom_id)).exists():
                messages.error(request, 'A lesson with that order already exists.')
            else:
                # save the lesson without committing to the database
                lesson = form.save(commit=False)
                # this allows us to add the teacher to the lesson
                lesson.teacher = request.user.teacher
                lesson.classroom = classroom
                lesson.save()
                
                return redirect('classroom:teacherClassroom', classroom_id=classroom_id)
            
            return render(request, 'classroom/newLesson.html', {
                'form': form,
                'classroom': classroom,
                
            })
            
    form = LessonForm()
    return render(request, 'classroom/newLesson.html', {
        'form': form,
        'classroom': classroom,
        })
    
@login_required
@allowed_users(allowed_roles=['TEACHER'])
def editLesson(request, classroom_id, lesson_id):
    classroom = Classroom.objects.get(id=classroom_id)
    lesson = Lesson.objects.get(id=lesson_id)
    if lesson.classroom.teacher != request.user.teacher:
        messages.error(request, 'You do not have permission to edit this lesson.')
        return redirect('classroom:teacher')
    
    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            notOriginal = False
            # check if order is in changed data
            if 'order' in form.changed_data:
                notOriginal = True
            # check if the order and classroom combination already exists
            if Lesson.objects.filter(order=form.cleaned_data['order'], classroom=Classroom.objects.get(id=classroom_id)).exists() and notOriginal:
                messages.error(request, 'A lesson with that order already exists.')
            else:
                form.save()
                return redirect('classroom:teacherClassroom', classroom_id=classroom_id)
    form = LessonForm(instance=lesson)
    return render(request, 'classroom/editLesson.html', {
        'form': form,
        'classroom': classroom,
        'lesson': lesson,
        })

@login_required
@allowed_users(allowed_roles=['TEACHER'])
def deleteLesson(request, classroom_id, lesson_id):
    classroom = Classroom.objects.get(id=classroom_id)
    lesson = Lesson.objects.get(id=lesson_id)
    if lesson.classroom.teacher != request.user.teacher:
        messages.error(request, 'You do not have permission to delete this lesson.')
        return redirect('classroom:teacher')
    
    lesson.delete()
    return redirect('classroom:teacherClassroom', classroom_id=classroom_id)
