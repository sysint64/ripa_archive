from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static

from ripa_archive import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^documents/', include('ripa_archive.documents.urls', namespace="documents"))
]


if settings.DEBUG:
    urlpatterns += [
        url(r'^layout/(?P<template>[A-z0-9_\-.]+)/$', views.layout),
    ]

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
