# Generated by Django 2.1.5 on 2019-06-16 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0108_auto_20190616_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monetization',
            name='bank',
            field=models.CharField(choices=[('first', 'First Bank Plc'), ('polaris', 'Polaris Bank Plc'), ('gt', 'GT Bank Plc'), ('access', 'Access Bank Plc'), ('zenith', 'Zenith Bank Plc')], default='gt', max_length=20),
        ),
    ]
