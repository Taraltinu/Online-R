# Generated by Django 3.1 on 2021-04-30 07:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('campany', '0012_auto_20210430_1216'),
    ]

    operations = [
        migrations.AddField(
            model_name='add_degree',
            name='candidate',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
