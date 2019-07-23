from django.contrib import admin
from .models import Post, Comment, Share, Report, HashTag, ShareTag

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'id', 'date_posted', 'restrict_comment')
    search_fields = ('user__username', 'title')
    date_hierarchy = ('date_posted')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'timestamp')


class ShareAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'date_posted')

class ReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'shared_post')

class HashTagAdmin(admin.ModelAdmin):
    list_display = ('user', 'post' , 'tag')

class ShareTagAdmin(admin.ModelAdmin):
    list_display = ('user', 'share' , 'tag')

admin.site.register(HashTag, HashTagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Share, ShareAdmin)
admin.site.register(ShareTag, ShareTagAdmin)
admin.site.register(Report, ReportAdmin)