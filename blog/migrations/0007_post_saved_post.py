# Generated by Django 2.1.7 on 2019-03-27 09:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0006_post_restrict_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='saved_post',
            field=models.ManyToManyField(blank=True, related_name='saved_post', to=settings.AUTH_USER_MODEL),
        ),
    ]
