from django.contrib import admin
from django.urls import path, include
from .views import (AllJobs, 
                    CreateJobOpening, 
                    SaveJobAPIToggle, 
                    SaveJobToggle, 
                    JobDetail, 
                    JobUpdateView, 
                    DeleteJobView, 
                    ShareJobView, 
                    ShareJobThread,
                    DeleteShareJob,
                    ShareJobUpdateView,
                    LikeShareApiToggle,
                    LikeShareJobToggle,
                    QuoteJobShare,
                    RequestJob
                    )


urlpatterns = [
    path('',AllJobs.as_view(),name='all_jobs'),
    path('new/', CreateJobOpening.as_view(), name='new_job'),
    path('<int:pk>/detail', JobDetail.as_view(), name='job-detail'),
    path('<int:pk>/update', JobUpdateView.as_view(), name='job-update'),
    path('<int:pk>/delete', DeleteJobView.as_view(), name='job-delete'),

    path('job/<int:pk>/save/', SaveJobAPIToggle.as_view(), name='save-job-api-toggle'),
    path('api/job/<int:pk>/save/', SaveJobToggle.as_view(), name='save-job-toggle'),

    path('<int:pk>/thread', ShareJobThread.as_view(), name='job-thread'),
    path('<int:pk>/share', ShareJobView.as_view(), name='job-share'),
    path('<int:pk>/quote', QuoteJobShare.as_view(), name='quote-share-job'),    
    path('request', RequestJob.as_view(), name='request-job'),
    path('<int:pk>/share/delete', DeleteShareJob.as_view(), name='job-share-delete'),
    path('<int:pk>/share/update', ShareJobUpdateView.as_view(), name='job-share-update'),
    path('<int:pk>/share/like', LikeShareJobToggle.as_view(), name='share-job-like-toggle'),
    path('api/share/<int:pk>/like', LikeShareApiToggle.as_view(), name='share-job-like-api-toggle'),    
]