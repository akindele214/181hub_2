# Generated by Django 2.1.5 on 2019-05-08 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0090_auto_20190508_2118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monetization',
            name='bank',
            field=models.CharField(choices=[('access', 'Access Bank Plc'), ('zenith', 'Zenith Bank Plc'), ('polaris', 'Polaris Bank Plc'), ('gt', 'GT Bank Plc'), ('first', 'First Bank Plc')], default='gt', max_length=20),
        ),
    ]
