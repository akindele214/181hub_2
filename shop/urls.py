from django.urls import path, include
from .views import  (CreateProductView, 
                    AdList, 
                    ViewProductDetail, 
                    ProductLikeToggle, 
                    ProductLikeAPIToggle,
                    ProductSaveToggle,
                    ProductSaveAPIToggle,
                    SavedAdListView,
                    UserAdView,
                    CategoryList,
                    AdDeleteView)


urlpatterns = [
    path('ads/', AdList.as_view(), name='all-ads'),
    path('ads/<int:pk>/', ViewProductDetail.as_view(), name='ad-detail'),
    path('create/', CreateProductView.as_view(), name='post-ad'),
    path('ad/<int:pk>/delete', AdDeleteView.as_view(), name='delete-ad'),
    path('saved/', SavedAdListView.as_view(), name='saved-ad'),
    path('myads/', UserAdView.as_view(), name='my-ads'),
    path('category/<str:category>/', CategoryList.as_view(), name='ad-category'),
    path('ad/<int:pk>/like/', ProductLikeToggle.as_view(), name='ad-like-toggle'),
    path('api/ad/<int:pk>/like/', ProductLikeAPIToggle.as_view(), name='ad-like-api-toggle'),
    path('ad/<int:pk>/save/', ProductSaveToggle.as_view(), name='ad-save-toggle'),
    path('api/ad/<int:pk>/save/', ProductSaveAPIToggle.as_view(), name='ad-save-api-toggle'),
]