# Generated by Django 2.1.7 on 2019-04-16 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0027_auto_20190416_1119'),
    ]

    operations = [
        migrations.RenameField(
            model_name='share',
            old_name='shared_by',
            new_name='user',
        ),
    ]
