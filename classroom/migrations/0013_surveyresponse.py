# Generated by Django 4.2.3 on 2023-08-08 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_student_classroom'),
        ('classroom', '0012_remove_lesson_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='SurveyResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_understanding', models.IntegerField(choices=[(1, 'Very well'), (2, 'Somewhat well'), (3, 'Not well')])),
                ('engagement', models.IntegerField(choices=[(1, 'Very engaged'), (2, 'Moderately engaged'), (3, 'Not very engaged')])),
                ('assessment_accuracy', models.BooleanField()),
                ('satisfaction', models.IntegerField(choices=[(1, 'Not satisfied at all'), (2, '2'), (3, '3'), (4, '4'), (5, 'Very satisfied')])),
                ('improvement_suggestions', models.TextField(blank=True, null=True)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.lesson')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.student')),
            ],
            options={
                'unique_together': {('lesson', 'student')},
            },
        ),
    ]
