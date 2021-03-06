# Generated by Django 2.1.5 on 2019-05-03 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0051_auto_20190503_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='monetized_views',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='monetization',
            name='bank',
            field=models.CharField(choices=[('access', 'Access Bank Plc'), ('gt', 'GT Bank Plc'), ('zenith', 'Zenith Bank Plc'), ('polaris', 'Polaris Bank Plc'), ('first', 'First Bank Plc')], default='gt', max_length=20),
        ),
    ]
