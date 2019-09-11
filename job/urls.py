from django.contrib import admin
from django.urls import path, include
from .views import AllJobs, CreateJobOpening

urlpatterns = [
    path('',AllJobs.as_view(),name='all_jobs'),
    path('new/', CreateJobOpening.as_view(), name='new_job'),
]