from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = 'STUDENT', 'Student'
        TEACHER = 'TEACHER', 'Teacher'
    
    base_role = Role.STUDENT
    
    role = models.CharField(max_length=50, choices=Role.choices, default=base_role)
    
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=10000.00)
    xp = models.IntegerField(default=0)
    
    def __str__(self):
        return self.user.username