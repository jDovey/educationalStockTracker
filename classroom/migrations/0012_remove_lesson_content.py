# Generated by Django 4.2.3 on 2023-08-03 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0011_lesson_lesson_outline'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='content',
        ),
    ]