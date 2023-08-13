from django.contrib import admin

from .models import Classroom, Lesson, SurveyResponse, QuizQuestion, QuizResponse, LessonQuizScore
# Register your models here.
admin.site.register(Classroom)
admin.site.register(Lesson)
admin.site.register(SurveyResponse)
admin.site.register(QuizQuestion)
admin.site.register(QuizResponse)
admin.site.register(LessonQuizScore)