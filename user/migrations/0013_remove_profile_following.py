# Generated by Django 2.1.7 on 2019-03-31 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_profile_following'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='following',
        ),
    ]
