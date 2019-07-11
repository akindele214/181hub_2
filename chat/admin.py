from django.contrib import admin
from .models import Message, ChatParticipants, Chat, ReportChat
# Register your models here.

class ChatAdmin(admin.ModelAdmin):
    list_display = ('id','chat_id',)

class ChatReport(admin.ModelAdmin):
    list_display = ('id', 'chat', 'user')


admin.site.register(Message)
admin.site.register(ChatParticipants)
admin.site.register(Chat, ChatAdmin)
admin.site.register(ReportChat, ChatReport)