from django.contrib import admin
from .models import Profile, Monetization, UserEmailRequest


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'user_id')


class MonAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'views', 'status', 'account_name', 'bank')


class EmailRequestAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'ref_code','date_added')

admin.site.register(Profile, UserAdmin)
admin.site.register(Monetization, MonAdmin)
admin.site.register(UserEmailRequest, EmailRequestAdmin)