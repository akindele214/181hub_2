# Generated by Django 2.2.4 on 2019-10-08 17:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0153_auto_20190911_1705'),
    ]

    operations = [
        migrations.CreateModel(
            name='Suggestion_Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('content', models.TextField()),
            ],
        ),
    ]
