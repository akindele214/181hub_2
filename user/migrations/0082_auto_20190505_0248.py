# Generated by Django 2.1.5 on 2019-05-05 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0081_auto_20190504_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monetization',
            name='bank',
            field=models.CharField(choices=[('polaris', 'Polaris Bank Plc'), ('access', 'Access Bank Plc'), ('zenith', 'Zenith Bank Plc'), ('first', 'First Bank Plc'), ('gt', 'GT Bank Plc')], default='gt', max_length=20),
        ),
    ]
