# Generated by Django 2.1.7 on 2019-04-03 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0026_auto_20190403_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='following',
            field=models.ManyToManyField(related_name='followin', to='user.Profile'),
        ),
    ]
