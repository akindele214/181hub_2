# Generated by Django 2.1.7 on 2019-04-08 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0034_auto_20190406_1503'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='content',
            field=models.TextField(blank=True, max_length=120),
        ),
    ]
