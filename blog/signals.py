from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Post
from user.models import Profile
from notifications.signals import notify


def my_handler(sender, instance, created, **kwargs):
    notify.send(instance, verb='liked you post')


post_save.connect(my_handler, sender=Post)

