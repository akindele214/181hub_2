# Generated by Django 2.2.4 on 2019-09-11 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0003_remove_jobopening_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobopening',
            name='send_cv_directly',
            field=models.BooleanField(default=False),
        ),
    ]
