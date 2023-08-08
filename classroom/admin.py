from django.contrib import admin

from .models import Classroom, Lesson, SurveyResponse
# Register your models here.
admin.site.register(Classroom)
admin.site.register(Lesson)
admin.site.register(SurveyResponse)