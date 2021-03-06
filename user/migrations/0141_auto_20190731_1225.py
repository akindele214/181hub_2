# Generated by Django 2.1.5 on 2019-07-31 11:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0140_adminupload'),
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='website_img/')),
            ],
        ),
        migrations.RemoveField(
            model_name='adminupload',
            name='image',
        ),
        migrations.AddField(
            model_name='images',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.AdminUpload'),
        ),
    ]
