# Generated by Django 2.1.5 on 2019-05-08 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0091_auto_20190508_2120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monetization',
            name='bank',
            field=models.CharField(choices=[('first', 'First Bank Plc'), ('gt', 'GT Bank Plc'), ('polaris', 'Polaris Bank Plc'), ('zenith', 'Zenith Bank Plc'), ('access', 'Access Bank Plc')], default='gt', max_length=20),
        ),
    ]
