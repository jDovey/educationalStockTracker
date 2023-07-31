from django.db import models

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
    short_description = models.CharField(max_length=100)
    long_description = models.TextField()
    
    def __str__(self):
        return self.title
    