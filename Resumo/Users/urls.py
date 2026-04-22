from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/',           views.register_view,           name='register'),
    path('login/',              views.login_view,               name='login'),
    path('logout/',             views.logout_view,              name='logout'),
    path('verify-email/',       views.verify_email_view,        name='verify_email'),
    path('resend-verification/',views.resend_verification_view, name='resend_verification'),
    path('dashboard/',          views.dashboard_view,           name='dashboard'),
]
