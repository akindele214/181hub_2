# Generated by Django 2.1.5 on 2019-08-06 11:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0072_auto_20190806_0638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grouppost',
            name='share_post',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='blog.GroupPost'),
        ),
    ]
