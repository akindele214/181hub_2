# Generated by Django 2.1.5 on 2019-06-21 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0112_auto_20190620_2039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monetization',
            name='bank',
            field=models.CharField(choices=[('first', 'First Bank Plc'), ('gt', 'GT Bank Plc'), ('polaris', 'Polaris Bank Plc'), ('access', 'Access Bank Plc'), ('zenith', 'Zenith Bank Plc')], default='gt', max_length=20),
        ),
    ]
