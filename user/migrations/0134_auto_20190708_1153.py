# Generated by Django 2.1.5 on 2019-07-08 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0133_auto_20190708_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monetization',
            name='status',
            field=models.CharField(choices=[('Cleared', 'Cleared'), ('uncleared', 'Uncleared')], default='uncleared', max_length=10),
        ),
    ]
