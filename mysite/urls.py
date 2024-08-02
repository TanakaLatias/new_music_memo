"""
accounts/login/ [name='account_login']
accounts/logout/ [name='account_logout']
accounts/inactive/ [name='account_inactive']
accounts/signup/ [name='account_signup']
accounts/confirm-email/ [name='account_email_verification_sent']
accounts/^confirm-email/(?P<key>[-:\w]+)/$ [name='account_confirm_email']
accounts/password/reset/ [name='account_reset_password']
accounts/password/reset/done/ [name='account_reset_password_done']
accounts/^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$ [name='account_reset_password_from_key']
accounts/password/reset/key/done/ [name='account_reset_password_from_key_done']

accounts/email/ [name='account_email']
accounts/reauthenticate/ [name='account_reauthenticate']
accounts/password/set/ [name='account_set_password']
accounts/password/change/ [name='account_change_password']
"""

from django.contrib import admin
from django.urls import path, include

from django.views.generic import TemplateView
class ErrorView(TemplateView):
    template_name = 'error.html'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/email/', ErrorView.as_view(), name='account_email'),
    path('accounts/reauthenticate/', ErrorView.as_view(), name='account_reauthenticate'),
    path('accounts/password/set/', ErrorView.as_view(), name='account_set_password'),
    path('accounts/password/change/', ErrorView.as_view(), name='account_change_password'),
    path('accounts/', include('allauth.urls')),
    path('', include('new_music_memo.urls')),
]