# Generated by Django 4.2.3 on 2023-07-08 17:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_holdings'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transactions',
            old_name='price',
            new_name='purchase_price',
        ),
    ]