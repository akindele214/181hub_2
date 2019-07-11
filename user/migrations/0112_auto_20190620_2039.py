# Generated by Django 2.1.5 on 2019-06-20 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0111_auto_20190620_2038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monetization',
            name='bank',
            field=models.CharField(choices=[('access', 'Access Bank Plc'), ('first', 'First Bank Plc'), ('polaris', 'Polaris Bank Plc'), ('gt', 'GT Bank Plc'), ('zenith', 'Zenith Bank Plc')], default='gt', max_length=20),
        ),
        migrations.AlterField(
            model_name='monetization',
            name='status',
            field=models.CharField(choices=[('Cleared', 'Cleared'), ('uncleared', 'Uncleared')], default='uncleared', max_length=10),
        ),
    ]
