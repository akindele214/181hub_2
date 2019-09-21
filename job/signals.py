from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import RequestJob
from blog.models import Post
from django.contrib.auth.models import User


@receiver(post_save, sender=RequestJob)
def after_job_create(sender, instance, created, **kwargs):
    if created:
        print("Saved")

@receiver(post_save, sender=RequestJob)
def save_post(sender, instance, **kwargs):
    print("SAVED")

post_save.connect(after_job_create, sender=RequestJob)

