from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.template.defaulttags import url

from django.conf.urls.static import static
from django.urls import path, re_path, include

from django.views.generic import TemplateView
from django.views.i18n import JavaScriptCatalog
from django.views.static import serve


from . import views

from .views import LoginUser, show_file, write_help, show_helps

urlpatterns = [
    path('', views.home, name='chat-home'),
    path('login/', auth_views.LoginView.as_view(template_name="chat/login.html"), name='chat-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name="chat/logout.html"), name='chat-logout'),
    path('register/', views.register, name='chat-register'),
    path('home/', views.home, name='chat-home'),
    path('profile/', views.profile, name='chat-profile'),
    path('send/', views.send_chat, name='chat-send'),
    path('renew/', views.get_messages, name='chat-renew'),
    path('post/',views.uploadFile,name='post'),
    re_path(r'^download/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path('buyfile/',views.buy_files,name='buyfile'),
    # path('register/', views.signup, name='chat-register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('invalid_verify/', TemplateView.as_view(template_name='chat/registration/invalid_verify.html'),
         name='invalid_verify'),
    path('nice_verify/', TemplateView.as_view(template_name='chat/registration/nice_verify.html'), name='nice_verify'),
    path('confirm_email/', TemplateView.as_view(template_name='chat/registration/confirm_email.html'), name="confirm_email"),
    path('', include('django.contrib.auth.urls')),
    path('file/<int:file_id>/',show_file,name='file'),
    path('help/',views.help,name='help'),
    path('write_help/',write_help, name = 'write_help'),
    path('find_help/', views.find_help, name = 'find_help'),
    path('help/<int:help_id>/', show_helps, name='help'),
    path('jsi18n', JavaScriptCatalog.as_view(),name = 'js-catlog',)

]
if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root =settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
