from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from classroom.models import Classroom

# Create your models here.

class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = 'STUDENT', 'Student'
        TEACHER = 'TEACHER', 'Teacher'
    
    base_role = Role.STUDENT
    
    role = models.CharField(max_length=50, choices=Role.choices, default=base_role)
    passwordTimeSet = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.username

# Create a student when a user is created
@receiver(post_save, sender=User)
def create_student(sender, instance, created, **kwargs):
    if created and instance.role == 'STUDENT':
        Student.objects.create(user=instance)
    
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    cash = models.DecimalField(max_digits=10, decimal_places=2, default=10000.00)
    total_value = models.DecimalField(max_digits=10, decimal_places=2, default=10000.00)
    xp = models.IntegerField(default=0)
    classroom = models.ForeignKey('classroom.Classroom', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.user.username
    
    # xp reward function
    def xpUp(self, xpGain):
        self.xp+=xpGain
        self.save()

# Create a teacher when a user is created
@receiver(post_save, sender=User)
def create_teacher(sender, instance, created, **kwargs):
    if created and instance.role == 'TEACHER':
        Teacher.objects.create(user=instance)

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    
    def __str__(self):
        return self.user.username