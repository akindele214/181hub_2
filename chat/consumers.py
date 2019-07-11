from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from asgiref.sync import async_to_sync
import json
from django.utils import timezone
from .models import Message,Chat
from django.contrib.auth import get_user_model
from .views import get_current_chat
from django.http import HttpResponseForbidden, Http404

User = get_user_model()


class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self,data):
        print(data['chatId'])
        messages = []
        current_user = User.objects.get(username=data['current_user'])
        chat = get_object_or_404(Chat, chat_id=data['chatId'])
        if current_user in chat.participants.all():
            message_unread = chat.messages.all()
            for message in message_unread:
                if message.author != current_user:
                    message.read = True
                    message.save()
                    messages.append(message)
                else: 
                    messages.append(message)
            #messages = chat.messages.all()
            content = {
                'command': 'messages',
                'messages': self.messages_to_json(messages)
            }
            self.send_message(content)
        else:
            pass

    def new_message(self, data):
        author = data['from']
        author_user = User.objects.get(username=author)
        current_chat = get_object_or_404(Chat, chat_id=data['chatId'])
        if author_user in current_chat.participants.all():
            if author_user == current_chat.receiver:
                message = Message.objects.create(author=author_user, content=data['message'])
                current_chat.messages.add(message)
                current_chat.receiver = None
                current_chat.accept = True
                current_chat.date_updated=timezone.now()
                current_chat.save()
                content = {
                    'command': 'new_message',
                    'message': self.message_to_json(message)
                }
                return self.send_chat_message(content)
            else:
                message = Message.objects.create(author=author_user, content=data['message'])
                current_chat.messages.add(message)
                current_chat.date_updated=timezone.now()
                current_chat.save()
                content = {
                    'command': 'new_message',
                    'message': self.message_to_json(message)
                }
                return self.send_chat_message(content)
        else:
            pass

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'id': message.id,
            'author': message.author.username,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))
