# Generated by Django 4.2.3 on 2023-08-09 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0016_rename_correctanswer_quizquestion_answer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizquestion',
            name='op3',
            field=models.CharField(default='op3', max_length=100),
        ),
    ]
