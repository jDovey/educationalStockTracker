from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Classroom(models.Model):
    name = models.CharField(max_length=100, unique=True)
    passcode = models.CharField(max_length=100)
    teacher = models.ForeignKey('user.Teacher', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Lesson(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'draft'
        PUBLISHED = 'PUBLISHED', 'published'
        
    class Meta:
        unique_together = ('order', 'classroom')
        
    base_status = Status.DRAFT
    
    status = models.CharField(max_length=50, choices=Status.choices, default=base_status)
    order = models.PositiveIntegerField(default = 0, blank = False, null = False)
    classroom = models.ForeignKey('classroom.Classroom', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=256)
    image = models.ImageField(upload_to='uploaded_images', blank=True, null=True)
    lesson_outline = models.JSONField(blank=True, null=True)
    
    def __str__(self):
        return self.title

class SurveyResponse(models.Model):
    class Meta:
        unique_together = ('lesson', 'student')
    
    lesson = models.ForeignKey('classroom.Lesson', on_delete=models.CASCADE)
    student = models.ForeignKey('user.Student', on_delete=models.CASCADE)
    content_understanding = models.IntegerField(choices=[
        (1, 'Very well'),
        (2, 'Somewhat well'),
        (3, 'Not well')
    ])
    
    engagement = models.IntegerField(choices=[
        (1, 'Very engaged'),
        (2, 'Moderately engaged'),
        (3, 'Not very engaged')
    ])
    
    assessment_accuracy = models.BooleanField()
    
    satisfaction = models.IntegerField(choices=[
        (1, 'Not satisfied at all'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, 'Very satisfied')
    ])
    
    improvement_suggestions = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.lesson.title + ' - ' + self.student.user.username
    
class QuizQuestion(models.Model):
    class Meta:
        unique_together = ('lesson', 'order')
        
    lesson = models.ForeignKey('classroom.Lesson', on_delete=models.CASCADE)
    question = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default = 0, blank = False, null = False)
    answer = models.CharField(max_length=100)
    op1 = models.CharField(max_length=100)
    op2 = models.CharField(max_length=100)
    op3 = models.CharField(max_length=100)
    
    def __str__(self):
        return self.question + ' - ' + self.lesson.title

class QuizResponse(models.Model):
    class Meta:
        unique_together = ('question', 'student')
    
    question = models.ForeignKey('classroom.QuizQuestion', on_delete=models.CASCADE)
    student = models.ForeignKey('user.Student', on_delete=models.CASCADE)
    answer = models.CharField(max_length=100)
    
    def __str__(self):
        return self.question.question + ' - ' + self.answer + ' - ' + self.student.user.username
    
class LessonQuizScore(models.Model):
    class Meta:
        unique_together = ('lesson', 'student')
        
    lesson = models.ForeignKey('classroom.Lesson', on_delete=models.CASCADE)
    student = models.ForeignKey('user.Student', on_delete=models.CASCADE)
    score = models.IntegerField()
    
class CommentMessage(models.Model):
    lesson = models.ForeignKey('classroom.Lesson', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('user.User', on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['created_at']
        
    def __str__(self):
        return self.content + ' - ' + self.created_by.username + ' - ' + self.lesson.title