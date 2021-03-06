# Generated by Django 2.1.5 on 2019-05-03 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0060_auto_20190503_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monetization',
            name='bank',
            field=models.CharField(choices=[('gt', 'GT Bank Plc'), ('polaris', 'Polaris Bank Plc'), ('first', 'First Bank Plc'), ('zenith', 'Zenith Bank Plc'), ('access', 'Access Bank Plc')], default='gt', max_length=20),
        ),
        migrations.AlterField(
            model_name='monetization',
            name='status',
            field=models.CharField(choices=[('uncleared', 'Uncleared'), ('Cleared', 'Cleared')], default='uncleared', max_length=10),
        ),
    ]
