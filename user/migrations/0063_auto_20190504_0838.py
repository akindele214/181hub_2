# Generated by Django 2.1.5 on 2019-05-04 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0062_auto_20190503_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monetization',
            name='bank',
            field=models.CharField(choices=[('gt', 'GT Bank Plc'), ('first', 'First Bank Plc'), ('access', 'Access Bank Plc'), ('zenith', 'Zenith Bank Plc'), ('polaris', 'Polaris Bank Plc')], default='gt', max_length=20),
        ),
    ]
