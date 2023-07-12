from django.db import models

# Create your models here.

class Classroom(models.Model):
    name = models.CharField(max_length=100, unique=True)
    passcode = models.CharField(max_length=100)
    teacher = models.ForeignKey('user.Teacher', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)