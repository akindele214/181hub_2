# Generated by Django 2.1.5 on 2019-07-08 10:38

from django.db import migrations, models
import profanity.validators


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0061_auto_20190703_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hashtag',
            name='tag',
            field=models.TextField(validators=[profanity.validators.validate_is_profane]),
        ),
        migrations.AlterField(
            model_name='quote',
            name='content',
            field=models.TextField(validators=[profanity.validators.validate_is_profane]),
        ),
        migrations.AlterField(
            model_name='report',
            name='content',
            field=models.TextField(validators=[profanity.validators.validate_is_profane]),
        ),
        migrations.AlterField(
            model_name='share',
            name='content',
            field=models.TextField(blank=True, null=True, validators=[profanity.validators.validate_is_profane]),
        ),
        migrations.AlterField(
            model_name='sharetag',
            name='tag',
            field=models.TextField(validators=[profanity.validators.validate_is_profane]),
        ),
    ]
