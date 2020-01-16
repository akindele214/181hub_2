from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import redirect, reverse
from hitcount.models import HitCount, HitCountMixin
from django.contrib.contenttypes.fields import GenericRelation

# REST FRAMEWORK
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions


class ShopManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = ( Q(prod_name__icontains = query)|
                         Q(prod_details__icontains=query)|
                         Q(prod_location__icontains=query)
                        ) 
            
            qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
        return qs


class Product(models.Model):

    CATEGORY_CHOICES = [
        ('', 'Select Field'),
        ('Accommodation', 'Accommodation'),
        ('Sound Devices', 'Sound Devices'),
        ('Cell/Mobile/Wireless Phones', 'Cell/Mobile/Wireless Phones'),
        ('Books', 'Books'),
        ('Computers', 'Computers'),
        ('TVs', 'TVs'),
        ('Cosmetics', 'Cosmetics'),
        ('Miscellaneous', 'Miscellaneous')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prod_name = models.CharField(max_length=70)
    prod_details = models.TextField()
    prod_price = models.CharField(max_length=25)
    prod_location = models.CharField(max_length=70)
    prod_category = models.CharField(choices=CATEGORY_CHOICES, max_length=30, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    phone_number = models.CharField(max_length=15, blank=True)
    # saved = models.ManyToManyField(User, related_name = 'saved_product', blank=True)
    cart = models.ManyToManyField(User, related_name = 'liked_product', blank=True)
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')
    objects = ShopManager()


    def __str__(self):
        return '{} - {}'.format(self.prod_name, str(self.user.username))


class ProductImage(models.Model):
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'prod_pic/', blank=True, null=True)

    def __str__(self):
        return self.prod.title
