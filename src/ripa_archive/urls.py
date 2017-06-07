from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static

from ripa_archive import views

urlpatterns = [
    url(r'^documents/', include('ripa_archive.documents.urls', namespace="documents")),
    url(r'^accounts/', include('ripa_archive.accounts.urls', namespace="accounts"))
]


if settings.DEBUG:
    urlpatterns += [
        url(r'^layout/(?P<template>[A-z0-9_\-.]+)/$', views.layout),
    ]

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
