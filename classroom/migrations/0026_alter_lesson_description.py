# Generated by Django 4.2.3 on 2023-08-24 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0025_alter_commentmessage_lesson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='description',
            field=models.CharField(max_length=256),
        ),
    ]