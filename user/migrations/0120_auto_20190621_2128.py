# Generated by Django 2.1.5 on 2019-06-21 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0119_auto_20190621_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monetization',
            name='bank',
            field=models.CharField(choices=[('zenith', 'Zenith Bank Plc'), ('gt', 'GT Bank Plc'), ('polaris', 'Polaris Bank Plc'), ('access', 'Access Bank Plc'), ('first', 'First Bank Plc')], default='gt', max_length=20),
        ),
        migrations.AlterField(
            model_name='monetization',
            name='status',
            field=models.CharField(choices=[('Cleared', 'Cleared'), ('uncleared', 'Uncleared')], default='uncleared', max_length=10),
        ),
    ]
