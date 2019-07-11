# Generated by Django 2.1.5 on 2019-05-10 10:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0049_auto_20190509_2128'),
    ]

    operations = [
        migrations.AddField(
            model_name='share',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='share_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
