from django.contrib import admin

from ripa_archive.documents.models import *


admin.site.register(Folder)
admin.site.register(Document)
admin.site.register(DocumentData)
admin.site.register(Status)