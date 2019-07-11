from django.contrib import admin
from django.urls import path, include
from user import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
import notifications.urls
from django.conf.urls import url
from chat import views as chat_views
from chat.views import ChatReport


urlpatterns = [
    path('admin/', admin.site.urls),
    path('live_counter/', user_views.live_counter, name='live_counter'),
    path('', include('blog.urls')),
    path('emoji/', include('emoji.urls')),
    url(r'^accounts/', include('allauth.urls')),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='user/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'), name='password_reset_complete'),
    path('profile/', user_views.profile, name='profile'),
    path('wallet/', user_views.wallet, name='wallet'),
    path('monetize/', user_views.monetize, name='monetize'),
    path('chat/', include('chat.urls')),
    path('directmessage/<int:receivers_id>/', chat_views.load_chat, name='message'),
    path('room/<int:room_name>/', chat_views.dm, name='dm'),
    path('<str:room_name>/', chat_views.room, name='room'),
    path('request/unaccepted/', chat_views.unaccepted_messages, name='unaccepted_messages'),
    path('room/messages/', chat_views.messages, name='messenger'),
    path('reportchat/<int:chat_id>', ChatReport.as_view(), name='report_chat'),
    path('room/delete/<int:chat_id>/', chat_views.delete_chat, name='delete_chat'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
