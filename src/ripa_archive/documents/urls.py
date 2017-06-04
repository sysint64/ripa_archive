from django.conf.urls import url

from ripa_archive.documents import views

urlpatterns = [
    url(r'^$', views.document_browser, name="browser"),
    url(r'^(?P<path>[0-9a-zA-Z /]+)/$', views.document_browser, name="browser"),
]
