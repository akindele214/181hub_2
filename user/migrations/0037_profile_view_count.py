# Generated by Django 2.1.5 on 2019-05-02 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0036_profile_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='view_count',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
