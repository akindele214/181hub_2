# Generated by Django 2.2.4 on 2019-09-12 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0011_jobopening_company_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobopening',
            name='state',
            field=models.CharField(max_length=140),
        ),
    ]
