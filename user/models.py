from django.db import models
from django.db.models import Q
# from django.contrib.auth.models import User, AbstractUser
from PIL import Image
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
from django.urls import reverse
from django.shortcuts import redirect
# from uuid import UUID
# Create your models here.


class ProfileManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query)|
                         Q(content__icontains=query)|
                         Q(user__username__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
        return qs

class AdminUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}'

class AdminImages(models.Model):
    admin = models.ForeignKey(AdminUpload, on_delete=models.CASCADE)
    image = models.FileField(upload_to='website_img/', blank=True, null=True)

    def __str__(self):
        return f'{self.admin}'

class Profile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=140, blank=True)
    content = models.TextField(max_length=120, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    following = models.ManyToManyField('self', related_name='followin', symmetrical=False)
    follower = models.ManyToManyField('self', related_name='followr', symmetrical=False)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    objects = ProfileManager()
    deleted_post_views = models.PositiveIntegerField(blank=False, null=False, default=0)
    monetized_views = models.IntegerField(blank=False, null=False, default=0)
    account_monetized = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'

    def get_absolute_url(self):
        return reverse('follower', kwargs={'user_id': self.user.id})

    def get_follow_url(self):
        return reverse('follow_toggle', kwargs={'user_id': self.user.id})

    def get_follow_api_url(self):
        return reverse('follow_api', kwargs={'user_id': self.user.id})

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Monetization(models.Model):
    STATUS_CHOICES = [
        ('uncleared', 'Uncleared'),
        ('Cleared', 'Cleared')
    ]
    BANK_CHOICES = [
        ('gt', 'GT Bank Plc'),
        ('first', 'First Bank Plc'),
        ('polaris', 'Polaris Bank Plc'),
        ('access', 'Access Bank Plc'),
        ('zenith', 'Zenith Bank Plc'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(blank=True, null=True)
    amount = models.PositiveIntegerField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='uncleared')
    bank = models.CharField(max_length=20, choices=BANK_CHOICES, default='gt')
    account_name = models.CharField(max_length=140)
    account_num = models.CharField(max_length=10)
    time_stamp = models.DateTimeField(default=timezone.now)
    transaction_ref = models.CharField(max_length=39, blank=False, unique=True, default=uuid.uuid4)

    def __str__(self):
        return '{} - {} - {} - {}'.format(str(self.user.username), self.views, self.amount, self.bank)

class UserEmailRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    #ref_code = models.CharField(max_legth=39, unique= True)
    ref_code = models.UUIDField(unique=True, default=uuid.uuid4,blank=False, editable=False)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{} - {}'.format(self.sender,self.receiver)
