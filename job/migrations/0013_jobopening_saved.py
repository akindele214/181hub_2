# Generated by Django 2.2.4 on 2019-09-13 04:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('job', '0012_auto_20190912_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobopening',
            name='saved',
            field=models.ManyToManyField(blank=True, related_name='saved_job', to=settings.AUTH_USER_MODEL),
        ),
    ]
