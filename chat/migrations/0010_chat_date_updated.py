# Generated by Django 2.1.5 on 2019-06-28 14:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0009_message_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='date_updated',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
