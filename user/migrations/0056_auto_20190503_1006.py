# Generated by Django 2.1.5 on 2019-05-03 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0055_auto_20190503_1005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monetization',
            name='account_num',
            field=models.CharField(default=1234567890, max_length=10),
        ),
        migrations.AlterField(
            model_name='monetization',
            name='bank',
            field=models.CharField(choices=[('gt', 'GT Bank Plc'), ('access', 'Access Bank Plc'), ('polaris', 'Polaris Bank Plc'), ('zenith', 'Zenith Bank Plc'), ('first', 'First Bank Plc')], default='gt', max_length=20),
        ),
    ]
