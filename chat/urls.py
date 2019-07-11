from django.contrib import admin
from django.urls import path, re_path

from .views import index, dm , room, load_chat

# app_name='chat'

urlpatterns = [
    path('', index, name='index'),
    
    # path('directmessage/<int:receivers_id>/', load_chat, name='message'),
    # path('room/<int:room_name>/', dm, name='dm'),
    # path('<str:room_name>/', room, name='room'),
    #re_path(r'^(?P<room_name>[^/]+)/$', room, name='room'),
]