# Generated by Django 2.1.5 on 2019-05-03 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0053_auto_20190503_1001'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='account_monetized',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='monetization',
            name='bank',
            field=models.CharField(choices=[('polaris', 'Polaris Bank Plc'), ('gt', 'GT Bank Plc'), ('zenith', 'Zenith Bank Plc'), ('access', 'Access Bank Plc'), ('first', 'First Bank Plc')], default='gt', max_length=20),
        ),
        migrations.AlterField(
            model_name='monetization',
            name='status',
            field=models.CharField(choices=[('uncleared', 'Uncleared'), ('Cleared', 'Cleared')], default='uncleared', max_length=10),
        ),
    ]
