# Generated by Django 2.2.4 on 2019-09-12 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0010_jobopening_job_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobopening',
            name='company_name',
            field=models.CharField(default='Facebook', max_length=140),
            preserve_default=False,
        ),
    ]
