# Generated by Django 2.1.5 on 2019-05-04 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0069_auto_20190504_0943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monetization',
            name='bank',
            field=models.CharField(choices=[('first', 'First Bank Plc'), ('gt', 'GT Bank Plc'), ('polaris', 'Polaris Bank Plc'), ('access', 'Access Bank Plc'), ('zenith', 'Zenith Bank Plc')], default='gt', max_length=20),
        ),
    ]
