# Generated by Django 2.1.5 on 2019-06-21 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0114_auto_20190621_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monetization',
            name='bank',
            field=models.CharField(choices=[('zenith', 'Zenith Bank Plc'), ('gt', 'GT Bank Plc'), ('first', 'First Bank Plc'), ('access', 'Access Bank Plc'), ('polaris', 'Polaris Bank Plc')], default='gt', max_length=20),
        ),
    ]
