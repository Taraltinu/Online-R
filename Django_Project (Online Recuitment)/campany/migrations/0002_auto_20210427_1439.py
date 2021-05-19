# Generated by Django 3.1 on 2021-04-27 09:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campany', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='phone',
            field=models.CharField(max_length=10, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number must be entered in the format +919999999999. Up to 10 digits allowed.', regex='^\\+?91?\\d{9,10}$')], verbose_name='Phone'),
        ),
    ]