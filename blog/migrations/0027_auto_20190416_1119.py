# Generated by Django 2.1.7 on 2019-04-16 10:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0026_auto_20190416_0712'),
    ]

    operations = [
        migrations.RenameField(
            model_name='share',
            old_name='user',
            new_name='shared_by',
        ),
    ]
