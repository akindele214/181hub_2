from django.urls import path, include
from .views import CreateProductView, AdList


urlpatterns = [
    path('ads/', AdList.as_view(), name='all-ads'),
    path('create/', CreateProductView.as_view(), name='post-ad')
]