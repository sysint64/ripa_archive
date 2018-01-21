from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.shortcuts import redirect

from forms.ajax import CompositeAjaxFormValidator
from ripa_archive import views, views_test
from ripa_archive.activity.views import users_activity
from ripa_archive.forms import SettingsForm
from ripa_archive.notifications.views import notifications
from ripa_archive.chat.views import chat
from ripa_archive.views_settings import settings_view
from ripa_archive.views_statistics import statistics


def redirect_to_browser(request):
    return redirect("documents:index")


urlpatterns = [
    url(r'^$', redirect_to_browser),
    url(r'^documents/', include('ripa_archive.documents.urls', namespace="documents")),
    url(r'^accounts/', include('ripa_archive.accounts.urls', namespace="accounts")),
    url(r'^permissions/', include('ripa_archive.permissions.urls', namespace="permissions")),
    url(r'^notifications/$', notifications, name="notifications"),
    url(r'^chat/$', chat, name="chat"),
    url(r'^activity/$', users_activity, name="activity"),
    url(r'^statistics/$', statistics, name="statistics"),
    url(r'^settings/$', settings_view, name="settings"),
    url(r'^help/$', views.help, name="help"),

    url(r'^!validator:settings/$',
        CompositeAjaxFormValidator.as_view(forms=[SettingsForm]),
        name="validator-settings"),
]


if settings.DEBUG:
    urlpatterns += [
        url(r'^layout/(?P<template>[A-z0-9_\-.]+)/$', views.layout),
    ]

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
