import os, django, random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cory_blog.settings')
django.setup()

from django.contrib.auth.models import User
from faker import Faker
from blog.models import Post
from django.contrib.auth.models import User
from django.utils import timezone


def create_post(N):
    fake = Faker()
    for fakes in range(N):
        id = random.randint(5, 8)
        title = fake.name()
        Post.objects.create(title=title,
                            author=User.objects.get(id=id),
                            content=fake.text(),
                            date_posted=timezone.now(),
                            )


create_post(100)
print('Data is populated successfully')

