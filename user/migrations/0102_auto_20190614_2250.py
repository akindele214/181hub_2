# Generated by Django 2.1.5 on 2019-06-14 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0101_auto_20190614_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monetization',
            name='bank',
            field=models.CharField(choices=[('zenith', 'Zenith Bank Plc'), ('gt', 'GT Bank Plc'), ('first', 'First Bank Plc'), ('polaris', 'Polaris Bank Plc'), ('access', 'Access Bank Plc')], default='gt', max_length=20),
        ),
    ]
