# Generated by Django 2.1.5 on 2019-08-06 04:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0070_grouppost_share_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='grouppost',
            name='seen_by',
            field=models.ManyToManyField(blank=True, related_name='seen', to=settings.AUTH_USER_MODEL),
        ),
    ]
