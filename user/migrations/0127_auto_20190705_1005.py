# Generated by Django 2.1.5 on 2019-07-05 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0126_auto_20190705_1001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monetization',
            name='bank',
            field=models.CharField(choices=[('access', 'Access Bank Plc'), ('zenith', 'Zenith Bank Plc'), ('first', 'First Bank Plc'), ('polaris', 'Polaris Bank Plc'), ('gt', 'GT Bank Plc')], default='gt', max_length=20),
        ),
    ]
