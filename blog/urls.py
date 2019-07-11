# from django.contrib import admin
from django.urls import path, include
from .views import (PostListView,
                    SavedPostListView,
                    saved_post_list,
                    home,
                    SearchView,
                    save_post, like_post,
                    PostCreateView,
                    PostUpdateView,
                    PostDeleteView,
                    ShareThread,
                    ShareView,
                    UserPostListView,
                    postdetail,
                    edit_post,
                    like_share,
                    view_following,
                    EditView,
                    ShareDeleteView,
                    CreatePostView,
                    PostDetailView,
                    HashSearchView,
                    MentionSearchView,
                    ShareEditView,
                    QuoteShare,
                    PostReport,
                    ShareReport,
                    user_post,
                    Trending)
from . import views
import notifications.urls
import hitcount.urls
from django.conf.urls import url

urlpatterns = [
    # POST
    path('', PostListView.as_view(), name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', EditView.as_view(), name='post-update'),
    path('post/<int:pk>/save_post/', views.save_post, name='save_post'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/new/', CreatePostView.as_view(), name='post-create'),
    path('create/', CreatePostView.as_view(), name='create-post'),
    path('like/', like_post, name='like_post'),
    path('saved/', SavedPostListView.as_view(), name='saved'),
    path('search/', SearchView.as_view(), name='blog-search'),
    path('hashtag/<str:hash>/', HashSearchView.as_view(), name='hash-search'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('mention/<str:username>/', MentionSearchView.as_view(), name='mention-posts'),
    path('report/<int:pk>/post/', PostReport.as_view(), name='report-post'),
    # path('trending/', Trending.as_view(), name='trending'),

    # SHARE    
    path('share-thread/<int:pk>/', ShareThread.as_view(), name='share-thread'),
    path('share/<int:pk>/delete/', ShareDeleteView.as_view(), name='share-delete'),
    path('share/<int:pk>/update/', ShareEditView.as_view(), name='share-edit'),
    path('share/<int:pk>/', ShareView.as_view(), name='share_post'),
    path('like_share/', like_share, name='like_share'),
    path('report/<int:pk>/share/', ShareReport.as_view(), name='report-share'),

    # QUOTE
    path('quote/<int:pk>/', QuoteShare.as_view(), name='quote-share'),

    # OTHERS
    path('follower/<int:user_id>/', views.follow, name='follower'),
    path('follower_list/<str:username>/', views.view_followers, name='follower_list'),
    path('following_list/<str:username>/', views.view_following, name='following_list'),
    path('notifications/', include(notifications.urls, namespace='notifications'), name='notifications'),
    path('hitcount/', include(hitcount.urls, namespace='hitcount')),


    # path('share/<int:pk>/', views.share_post, name='share_post'),
    # path('user/<str:username>', views.user_post, name='user-posts'),
    # path('post/<int:pk>/update/', views.edit_post, name='post-update'),
    # path('saved/', views.saved_post_list, name='saved'),
    # path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    # path('update/<int:pk>/', EditView.as_view(), name='edit-post'),
    # path('post/<int:pk>/', views.postdetail, name='post-detail'),
    # path('', views.home, name='blog-home'),
]
