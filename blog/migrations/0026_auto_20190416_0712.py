# Generated by Django 2.1.7 on 2019-04-16 06:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0025_share_date_posted'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'verbose_name': 'Post', 'verbose_name_plural': 'Posts'},
        ),
        migrations.AlterModelOptions(
            name='share',
            options={'verbose_name': 'Share', 'verbose_name_plural': 'Shares'},
        ),
    ]
