from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import formset_factory
from django.db.models import F

from user.models import Student
from .models import Classroom, Lesson, SurveyResponse, QuizQuestion, QuizResponse, LessonQuizScore
from user.decorators import allowed_users
from core.models import Holdings
from .forms import NewClassroomForm, JoinClassroomForm, EditStudentForm, LessonForm, LearningObjectiveFormSet, SurveyResponseForm, QuizQuestionFormSet, QuizQuestionForm, QuizResponseForm, QuizResponseFormSetBase

import json

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
    
    for lesson in classroomLessons:
        # check if there is an associated quiz
        lesson.has_quiz = QuizQuestion.objects.filter(lesson=lesson).exists()
        # get count of students who have completed the survey
        lesson.survey_responses = SurveyResponse.objects.filter(lesson=lesson).count()
        # get count of students who have completed the quiz
        lesson.quiz_responses = QuizResponse.objects.filter(question__lesson=lesson).values('student').distinct().count()
        
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
def resetStudent(request, student_id):
    student = Student.objects.get(user_id=student_id)
    if student.classroom.teacher != request.user.teacher:
        messages.error(request, 'You do not have permission to remove this student.')
        return redirect('classroom:teacher')
    # reset student values
    student.cash = 10000.00
    student.total_value = 10000.00
    student.save()
    # delete their holdings
    Holdings.objects.filter(student=student).delete()
    return redirect('classroom:teacherClassroom', classroom_id=student.classroom.id)

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
        form = LessonForm(request.POST, request.FILES)
        objective_forms = LearningObjectiveFormSet(request.POST, prefix=0)
        if form.is_valid() and all(form.is_valid() for form in objective_forms):
            # check if the order and classroom combination already exists
            if Lesson.objects.filter(order=form.cleaned_data['order'], classroom=Classroom.objects.get(id=classroom_id)).exists():
                messages.error(request, 'A lesson with that order already exists.')
            else:
                # save the lesson without committing to the database
                lesson = form.save(commit=False)
                # this allows us to add the teacher and the learning outline to the lesson
                lesson.teacher = request.user.teacher
                lesson.classroom = classroom
                
                
                learning_objectives = []
                for objective_form in objective_forms:
                    objective_text = objective_form.cleaned_data['learning_objective']
                    content_text = objective_form.cleaned_data['content']
                    learning_objectives.append({
                        'learning_objective': objective_text, 
                        'content': content_text
                        })
                lesson.lesson_outline = json.dumps(learning_objectives)
                lesson.save()
            
                return redirect('classroom:teacherClassroom', classroom_id=classroom_id)
            
            return render(request, 'classroom/newLesson.html', {
                'form': form,
                'objective_forms': objective_forms,
                'classroom': classroom,
                
            })
            
    form = LessonForm()
    objective_forms = LearningObjectiveFormSet(prefix=0)
    return render(request, 'classroom/newLesson.html', {
        'form': form,
        'objective_forms': objective_forms,
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
        form = LessonForm(request.POST, request.FILES, instance=lesson)
        objective_forms = LearningObjectiveFormSet(request.POST, prefix=0)
        
        if form.is_valid() and all(form.is_valid() for form in objective_forms):
            notOriginal = False
            # check if order is in changed data
            if 'order' in form.changed_data:
                notOriginal = True
            # check if the order and classroom combination already exists
            if Lesson.objects.filter(order=form.cleaned_data['order'], classroom=Classroom.objects.get(id=classroom_id)).exists() and notOriginal:
                messages.error(request, 'A lesson with that order already exists.')
            else:
                lessonEdit = form.save(commit=False)
                
                learning_objectives = []
                for objective_form in objective_forms:
                    objective_text = objective_form.cleaned_data['learning_objective']
                    content_text = objective_form.cleaned_data['content']
                    learning_objectives.append({
                        'learning_objective': objective_text, 
                        'content': content_text
                        })
                lessonEdit.lesson_outline = json.dumps(learning_objectives)
                lessonEdit.save()
                
                return redirect('classroom:teacherClassroom', classroom_id=classroom_id)
            
    form = LessonForm(instance=lesson)
    # get the lesson outline, ignore if it is None
    if lesson.lesson_outline:
        lesson_outline = json.loads(lesson.lesson_outline)
        # create a formset for the lesson outline
        objective_forms = LearningObjectiveFormSet(initial=lesson_outline, prefix=0)
    else:
        objective_forms = LearningObjectiveFormSet(prefix=0)
        
    return render(request, 'classroom/editLesson.html', {
        'form': form,
        'objective_forms': objective_forms,
        'classroom': classroom,
        'lesson': lesson,
        })

@login_required
@allowed_users(allowed_roles=['TEACHER'])
def deleteLesson(request, classroom_id, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    if lesson.classroom.teacher != request.user.teacher:
        messages.error(request, 'You do not have permission to delete this lesson.')
        return redirect('classroom:teacher')
    
    lesson.delete()
    return redirect('classroom:teacherClassroom', classroom_id=classroom_id)

@login_required
@allowed_users(allowed_roles=['STUDENT'])
def viewLesson(request, classroom_id, lesson_id):
    classroom = Classroom.objects.get(id=classroom_id)
    lesson = Lesson.objects.get(id=lesson_id)
    
    surveyComplete = False
    quizComplete = False
    
    # check if the student has already submitted a survey response for this lesson
    if SurveyResponse.objects.filter(lesson=lesson, student=request.user.student).exists():
        surveyComplete = True
        
    # check if the student has already submitted a quiz response for this lesson
    # get first question from lesson
    
    if QuizResponse.objects.filter(question__lesson=lesson, student=request.user.student).exists():
        quizComplete = True
        
    # check if the lesson has a lesson outline
    if lesson.lesson_outline:
        lesson_outline = json.loads(lesson.lesson_outline)
    else:
        lesson_outline = None
    
    if lesson.classroom != request.user.student.classroom or lesson.status != 'PUBLISHED':
        messages.error(request, 'You do not have permission to view this lesson.')
        return redirect('classroom:student')
    
    return render(request, 'classroom/viewLesson.html', {
        'classroom': classroom,
        'lesson': lesson,
        'lesson_outline': lesson_outline,
        'surveyComplete': surveyComplete,
        'quizComplete': quizComplete,
        })
    
@login_required
@allowed_users(allowed_roles=['TEACHER'])
def previewLesson(request, classroom_id, lesson_id):
    classroom = Classroom.objects.get(id=classroom_id)
    lesson = Lesson.objects.get(id=lesson_id)
    # check if the lesson has a lesson outline
    if lesson.lesson_outline:
        lesson_outline = json.loads(lesson.lesson_outline)
    else:
        lesson_outline = None
    
    if lesson.classroom.teacher != request.user.teacher:
        messages.error(request, 'You do not have permission to view this lesson.')
        return redirect('classroom:teacher')
    
    return render(request, 'classroom/viewLesson.html', {
        'classroom': classroom,
        'lesson': lesson,
        'lesson_outline': lesson_outline,
        })
    
@login_required
@allowed_users(allowed_roles=['STUDENT'])
def survey(request, classroom_id, lesson_id):
    classroom = Classroom.objects.get(id=classroom_id)
    lesson = Lesson.objects.get(id=lesson_id)
    
    if lesson.classroom != request.user.student.classroom or lesson.status != 'PUBLISHED':
        messages.error(request, 'You do not have permission.')
        return redirect('classroom:student')
    
    if request.method == 'POST':
        form = SurveyResponseForm(request.POST)
        if form.is_valid():
            # check if the student has already submitted a survey response for this lesson
            if SurveyResponse.objects.filter(lesson=lesson, student=request.user.student).exists():
                messages.error(request, 'You have already submitted a survey response for this lesson.')
                return redirect('classroom:viewLesson', classroom_id=classroom_id, lesson_id=lesson_id)
            # save the survey response without committing to the database
            surveyResponse = form.save(commit=False)
            # this allows us to add the lesson and student to the survey response
            surveyResponse.lesson = lesson
            surveyResponse.student = request.user.student
            surveyResponse.save()

            messages.success(request, 'You have successfully submitted your survey response.')
            return redirect('classroom:viewLesson', classroom_id=classroom_id, lesson_id=lesson_id)
    
    form = SurveyResponseForm()
    return render(request, 'classroom/survey.html', {
        'classroom': classroom,
        'lesson': lesson,
        'form': form,
        })

@login_required
@allowed_users(allowed_roles=['TEACHER'])
def newQuiz(request, classroom_id, lesson_id):
    classroom = Classroom.objects.get(id=classroom_id)
    lesson = Lesson.objects.get(id=lesson_id)
    
    if lesson.classroom.teacher != request.user.teacher:
        messages.error(request, 'You do not have permission to create a quiz for this lesson.')
        return redirect('classroom:teacher')
    
    if request.method == 'POST':
        quiz_forms = QuizQuestionFormSet(request.POST, prefix=0)
        if all(form.is_valid() for form in quiz_forms):
            for form in quiz_forms:
                # check if a quiz question with that order already exists
                if QuizQuestion.objects.filter(lesson=lesson, order=form.cleaned_data['order']).exists():
                    messages.error(request, 'A quiz question with that order already exists.')
                    return redirect('classroom:newQuiz', classroom_id=classroom_id, lesson_id=lesson_id)
                
                # save the quiz question without committing to the database
                quiz = form.save(commit=False)
                # this allows us to add the lesson to the quiz question
                quiz.lesson = lesson
                quiz.save()
            
            return redirect('classroom:teacherClassroom', classroom_id=classroom_id)
    
    quiz_forms = QuizQuestionFormSet(prefix=0)
    return render(request, 'classroom/newQuiz.html', {
        'classroom': classroom,
        'lesson': lesson,
        'quiz_forms': quiz_forms,
        })

@login_required
@allowed_users(allowed_roles=['TEACHER'])
def editQuiz(request, classroom_id, lesson_id):
    classroom = Classroom.objects.get(id=classroom_id)
    lesson = Lesson.objects.get(id=lesson_id)
    quiz_questions = QuizQuestion.objects.filter(lesson=lesson).order_by('order')
    
    return render(request, 'classroom/editQuiz.html', {
        'classroom': classroom,
        'lesson': lesson,
        'quiz_questions': quiz_questions,
        })

@login_required
@allowed_users(allowed_roles=['TEACHER'])
def editQuizQuestion(request, classroom_id, lesson_id, question_id):
    classroom = Classroom.objects.get(id=classroom_id)
    lesson = Lesson.objects.get(id=lesson_id)
    quizQuestion = QuizQuestion.objects.get(id=question_id)
    
    if request.method == 'POST':
        form = QuizQuestionForm(request.POST, instance=quizQuestion)
        if form.is_valid():
            notOriginal = False
            # check if order is in changed data
            if 'order' in form.changed_data:
                notOriginal = True
            # check if a quiz question with that order already exists
            if QuizQuestion.objects.filter(lesson=lesson, order=form.cleaned_data['order']).exists() and notOriginal:
                messages.error(request, 'A quiz question with that order already exists.')
                return redirect('classroom:editQuizQuestion', classroom_id=classroom_id, lesson_id=lesson_id, question_id=question_id)

            form.save()
            return redirect('classroom:editQuiz', classroom_id=classroom_id, lesson_id=lesson_id)
    
    form = QuizQuestionForm(instance=quizQuestion)
    
    return render(request, 'classroom/editQuizQuestion.html', {
        'classroom': classroom,
        'lesson': lesson,
        'quizQuestion': quizQuestion,
        'form': form,
        })

@login_required
@allowed_users(allowed_roles=['TEACHER'])
def deleteQuizQuestion(request, classroom_id, lesson_id, question_id):
    # check if the quiz question belongs to the teacher
    if QuizQuestion.objects.get(id=question_id).lesson.classroom.teacher != request.user.teacher:
        messages.error(request, 'You do not have permission to delete this quiz question.')
        return redirect('classroom:teacher')
    quizQuestion = QuizQuestion.objects.get(id=question_id)
    quizQuestion.delete()
    return redirect('classroom:editQuiz', classroom_id=classroom_id, lesson_id=lesson_id)

@login_required
@allowed_users(allowed_roles=['TEACHER'])
def addQuizQuestion(request, classroom_id, lesson_id):
    classroom = Classroom.objects.get(id=classroom_id)
    lesson = Lesson.objects.get(id=lesson_id)
    
    if request.method == 'POST':
        form = QuizQuestionForm(request.POST)
        if form.is_valid():
            # check if a quiz question with that order already exists
            if QuizQuestion.objects.filter(lesson=lesson, order=form.cleaned_data['order']).exists():
                messages.error(request, 'A quiz question with that order already exists.')
                return redirect('classroom:addQuizQuestion', classroom_id=classroom_id, lesson_id=lesson_id)
            
            # save the quiz question without committing to the database
            quiz = form.save(commit=False)
            # this allows us to add the lesson to the quiz question
            quiz.lesson = lesson
            quiz.save()
            
            return redirect('classroom:editQuiz', classroom_id=classroom_id, lesson_id=lesson_id)
    
    form = QuizQuestionForm()
    return render(request, 'classroom/addQuizQuestion.html', {
        'classroom': classroom,
        'lesson': lesson,
        'form': form,
        })
    
@login_required
@allowed_users(allowed_roles=['STUDENT'])
def takeQuiz(request, classroom_id, lesson_id):
    classroom = Classroom.objects.get(id=classroom_id)
    lesson = Lesson.objects.get(id=lesson_id)
    quiz = QuizQuestion.objects.filter(lesson=lesson).order_by('order')
    
    if len(quiz) == 0:
        messages.error(request, 'There is no quiz for this lesson.')
        return redirect('classroom:viewLesson', classroom_id=classroom_id, lesson_id=lesson_id)
    
    # if the student has already submitted a quiz response for this lesson, redirect them to the lesson page
    if QuizResponse.objects.filter(question__lesson=lesson, student=request.user.student).exists():
        messages.error(request, 'You have already submitted a quiz response for this lesson.')
        return redirect('classroom:viewLesson', classroom_id=classroom_id, lesson_id=lesson_id)
    
    QuizResponseFormSet = formset_factory(QuizResponseForm, formset=QuizResponseFormSetBase, extra=len(quiz))
    
    if request.method == 'POST':
        forms = QuizResponseFormSet(request.POST, prefix=0, question_list=quiz)
        if forms.is_valid():
            score = 0
            for i, form in enumerate(forms):
                questionObj = quiz[i]
                answer = form.cleaned_data[str(questionObj.question)]
                
                quiz_response = QuizResponse(
                    question=questionObj,
                    student=request.user.student,
                    answer=answer,
                )
                quiz_response.save()
                # check if the answer is correct
                if answer == questionObj.answer:
                    score += 1
            
            # store the score
            lessonScore = LessonQuizScore.objects.create(
                lesson=lesson,
                student=request.user.student,
                score=score,
            )
            lessonScore.save()
            
            # update the students xp based on the % of questions they got correct
            # get the total number of questions
            numQuestions = len(quiz)
            correctPercent = (score / numQuestions) * 100
            # update students xp
            student = request.user.student
            student.xp = F("xp") + correctPercent
            student.save()
            # create a message to display to the student
            messages.success(request, 'You have successfully submitted your quiz response. You got %d out of %d questions correct.' % (score, numQuestions))
            
        return redirect('classroom:studentClassroom', classroom_id=classroom_id)
    
    forms = QuizResponseFormSet(prefix=0, question_list=quiz)
    
    return render(request, 'classroom/quiz.html', {
        'classroom': classroom,
        'lesson': lesson,
        'quiz': quiz,
        'forms': forms,
        })
    
@login_required
@allowed_users(allowed_roles=['STUDENT'])
def viewQuizResults(request, classroom_id, lesson_id):
    classroom = Classroom.objects.get(id=classroom_id)
    lesson = Lesson.objects.get(id=lesson_id)
    quiz = QuizQuestion.objects.filter(lesson=lesson).order_by('order')
    
    if len(quiz) == 0:
        messages.error(request, 'There is no quiz for this lesson.')
        return redirect('classroom:viewLesson', classroom_id=classroom_id, lesson_id=lesson_id)
    
    # if the student has not submitted a quiz response for this lesson, redirect them to the lesson page
    if not QuizResponse.objects.filter(question__lesson=lesson, student=request.user.student).exists():
        messages.error(request, 'You have not submitted a quiz response for this lesson.')
        return redirect('classroom:viewLesson', classroom_id=classroom_id, lesson_id=lesson_id)
    
    # get the students quiz responses
    quiz_responses = QuizResponse.objects.filter(question__lesson=lesson, student=request.user.student).order_by('question__order')
    
    # get the students quiz score
    quiz_score = LessonQuizScore.objects.get(lesson=lesson, student=request.user.student)
    
    return render(request, 'classroom/viewQuizResults.html', {
        'classroom': classroom,
        'lesson': lesson,
        'quiz': quiz,
        'quiz_responses': quiz_responses,
        'quiz_score': quiz_score,
        })