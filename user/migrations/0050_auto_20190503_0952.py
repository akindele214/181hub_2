# Generated by Django 2.1.5 on 2019-05-03 08:52

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0049_auto_20190503_0452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monetization',
            name='bank',
            field=models.CharField(choices=[('gt', 'GT Bank Plc'), ('zenith', 'Zenith Bank Plc'), ('access', 'Access Bank Plc'), ('first', 'First Bank Plc'), ('polaris', 'Polaris Bank Plc')], default='gt', max_length=20),
        ),
        migrations.AlterField(
            model_name='monetization',
            name='transaction_ref',
            field=models.CharField(default=uuid.uuid4, max_length=39, unique=True),
        ),
    ]
