# Generated by Django 3.1 on 2021-04-28 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campany', '0007_auto_20210428_1530'),
    ]

    operations = [
        migrations.AddField(
            model_name='add_job_model',
            name='ex_p',
            field=models.CharField(default='1.5 year', max_length=20),
            preserve_default=False,
        ),
    ]
