# Generated by Django 2.1.5 on 2019-07-08 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0132_auto_20190708_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monetization',
            name='bank',
            field=models.CharField(max_length=20),
        ),
    ]
