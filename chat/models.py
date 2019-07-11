from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils import timezone
# Create your models here.


class Message(models.Model):
    author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField()
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username
    
    def last_10_messages():
        return Message.objects.order_by('timestamp').all()[:10]


class Contact(models.Model):
    user = models.ForeignKey(User, related_name='friends',on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', blank=True)



class ChatParticipants(models.Model):
    participants = models.ForeignKey(User, related_name='group_members', on_delete=models.CASCADE)
    group_members = models.ManyToManyField('self', blank=True)

class Messages(models.Model):
    contact = models.ForeignKey(ChatParticipants, related_name="messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  self.contact.user.username


class Chat(models.Model):
    chat_id = models.CharField(max_length=20, unique=True)
    participants = models.ManyToManyField(User, related_name='chat', blank=True)
    deleted = models.ManyToManyField(User, related_name='deleted_by', blank=True)
    messages = models.ManyToManyField(Message, blank=True)
    date_updated = models.DateTimeField(default=timezone.now)
    accept = models.BooleanField(default=False)
    initiator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='init')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver', blank=True, null=True)
    def __str__(self):
        return "{}".format(self.pk)

class ReportChat(models.Model):
    chat = models.ForeignKey(Chat, related_name='report_chat', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return "{} - {}".format(self.chat, self.user)