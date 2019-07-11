# Generated by Django 2.1.5 on 2019-07-10 12:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0016_auto_20190710_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='chat', to=settings.AUTH_USER_MODEL),
        ),
    ]
