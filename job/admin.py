from django.contrib import admin
from .models import JobOpening
# Register your models here.


class JobAdmin(admin.ModelAdmin):
    list_display = ( 'user', 'id', 'company_name', 'job_title','date_posted')
    search_fields = ('user__username', 'title')
    date_hierarchy = ('date_posted')

admin.site.register(JobOpening, JobAdmin)