from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.shortcuts import redirect

from ripa_archive import views


def redirect_to_browser(request):
    return redirect("documents:browser")


urlpatterns = [
    url(r'^$', redirect_to_browser),
    url(r'^search/', include('haystack.urls')),
    url(r'^documents/', include('ripa_archive.documents.urls', namespace="documents")),
    url(r'^accounts/', include('ripa_archive.accounts.urls', namespace="accounts"))
]


if settings.DEBUG:
    urlpatterns += [
        url(r'^layout/(?P<template>[A-z0-9_\-.]+)/$', views.layout),
    ]

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
