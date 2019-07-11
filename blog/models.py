from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import redirect
from django.db.models import Q
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCount, HitCountMixin
from profanity.validators import validate_is_profane
from taggit.managers import TaggableManager
from django.core.validators import FileExtensionValidator
from django.utils.encoding import python_2_unicode_compatible
from PIL import Image
# Create your models here.


class PostManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query)|
                         Q(content__icontains=query)|
                         Q(user__username__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
        return qs


@python_2_unicode_compatible
class Post(models.Model, HitCountMixin):
    title = models.CharField(max_length=140,validators=[validate_is_profane])
    content = models.TextField(validators=[validate_is_profane])
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.FileField(upload_to='uploads/', blank=True, null=True, validators=[FileExtensionValidator(["mp4"])])
    restrict_comment = models.BooleanField(default=False)
    saved = models.ManyToManyField(User, related_name='saved_post', blank=True)
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')
    objects = PostManager()

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class Images(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_pic/', blank=True, null=True)

    def __str__(self):
        return self.post.title + ' Image'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey('self', null=True, related_name='replies', on_delete=models.CASCADE)
    content = models.TextField(max_length=160,validators=[validate_is_profane])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.post.title, str(self.user.username))


class Share(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField(validators=[validate_is_profane], null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='share_likes', blank=True)
    image = models.ImageField(upload_to='shared_pic/', blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    is_quote = models.BooleanField(default=False)
    share_post = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return '{}- {}'.format(self.post.title, str(self.user.username))

    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('share-thread', kwargs={'pk': self.post.pk})

    class Meta:
        verbose_name = 'Share'
        verbose_name_plural = 'Shares'


class HashTag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=123)
    tag = models.TextField(validators=[validate_is_profane])
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{} - {}'.format(self.post, str(self.tag))


class ShareTag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    share = models.ForeignKey(Share, on_delete=models.CASCADE)
    tag = models.TextField(validators=[validate_is_profane])
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{}- {}'.format(self.share, str(self.tag))

class Quote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    share_post = models.ForeignKey(Share, on_delete=models.CASCADE)
    content = models.TextField(validators=[validate_is_profane])
    image = models.ImageField(upload_to='quote_pic/', blank=True, null=True)
    date_posted = models.DateField(default=timezone.now)
    # objects = models.Manager() 
    def __str__(self):
        return '{} - {}'.format(self.share_post, str(self.user.username))

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shared_post = models.ForeignKey(Share, on_delete=models.CASCADE, blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField(validators=[validate_is_profane])
    date_submited = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{} - {}'.format(str(self.user.username), self.date_submited)
