# Generated by Django 2.2.4 on 2020-01-17 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_auto_20200116_2219'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='cart',
            new_name='save',
        ),
    ]