from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Post
from user.models import Profile
from notifications.signals import notify


# def my_handler(sender, instance, created, **kwargs):
#     notify.send(instance, verb='liked you post')


# post_save.connect(my_handler, sender=Post)

@receiver(post_save, sender=Post)
def after_job_create(sender, instance, created, **kwargs):
    if created:
        print("Saved")

@receiver(post_save, sender=Post)
def save_post(sender, instance, **kwargs):
    print("SAVED")

post_save.connect(save_post, sender=Post)