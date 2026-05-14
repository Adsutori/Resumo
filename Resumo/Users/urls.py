from django.urls import path
from . import views
from Notifications.utils import notify_welcome, notify_feature

app_name = 'users'

urlpatterns = [
    path('register/',           views.register_view,           name='register'),
    path('login/',              views.login_view,               name='login'),
    path('logout/',             views.logout_view,              name='logout'),
    path('verify-email/',       views.verify_email_view,        name='verify_email'),
    path('resend-verification/',views.resend_verification_view, name='resend_verification'),
    path('settings/',               views.settings_view,   name='settings'),
    path('settings/nick/',          views.change_nick,     name='change_nick'),
    path('settings/email/',         views.change_email,    name='change_email'),
    path('settings/password/',      views.change_password, name='change_password'),
    path('settings/avatar/',        views.upload_avatar,   name='upload_avatar'),
    path('settings/delete/',        views.delete_account,  name='delete_account'),
    path('help',               views.help_view,           name='help'),
]
