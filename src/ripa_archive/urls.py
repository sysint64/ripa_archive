from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.shortcuts import redirect

from ripa_archive import views
from ripa_archive.activity.views import users_activity
from ripa_archive.notifications.views import notifications


def redirect_to_browser(request):
    return redirect("documents:index")


urlpatterns = [
    url(r'^$', redirect_to_browser),
    url(r'^documents/', include('ripa_archive.documents.urls', namespace="documents")),
    url(r'^accounts/', include('ripa_archive.accounts.urls', namespace="accounts")),
    url(r'^permissions/', include('ripa_archive.permissions.urls', namespace="permissions")),
    url(r'^notifications/$', notifications, name="notifications"),
    url(r'^activity/$', users_activity, name="activity"),
]


if settings.DEBUG:
    urlpatterns += [
        url(r'^layout/(?P<template>[A-z0-9_\-.]+)/$', views.layout),
    ]

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
