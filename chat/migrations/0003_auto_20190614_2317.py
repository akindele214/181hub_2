# Generated by Django 2.1.5 on 2019-06-14 22:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0002_auto_20190614_2250'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatParticipants',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_members', models.ManyToManyField(blank=True, related_name='_chatparticipants_group_members_+', to='chat.ChatParticipants')),
                ('participants', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_members', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='chat',
            name='participants',
            field=models.ManyToManyField(related_name='chat', to='chat.ChatParticipants'),
        ),
        migrations.AlterField(
            model_name='messages',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat.ChatParticipants'),
        ),
    ]
