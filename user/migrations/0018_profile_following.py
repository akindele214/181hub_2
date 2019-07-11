# Generated by Django 2.1.7 on 2019-04-03 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0017_remove_profile_following'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='_profile_following_+', to='user.Profile'),
        ),
    ]
