# Generated by Django 2.1.5 on 2019-06-14 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0100_auto_20190613_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monetization',
            name='bank',
            field=models.CharField(choices=[('zenith', 'Zenith Bank Plc'), ('first', 'First Bank Plc'), ('polaris', 'Polaris Bank Plc'), ('access', 'Access Bank Plc'), ('gt', 'GT Bank Plc')], default='gt', max_length=20),
        ),
        migrations.AlterField(
            model_name='monetization',
            name='status',
            field=models.CharField(choices=[('Cleared', 'Cleared'), ('uncleared', 'Uncleared')], default='uncleared', max_length=10),
        ),
    ]
