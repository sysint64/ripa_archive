from celery_haystack.indexes import CelerySearchIndex
from django.template import Context
from django.template import loader
from haystack import indexes
from ripa_archive.documents.models import Folder, Document


def _parent_ids(object):
    parents = []
    parent = object.parent

    while parent is not None:

        parents.append(parent.pk)
        parent = parent.parent

    return parents


class FolderIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(model_attr="name", document=True)
    suggestions = indexes.FacetCharField()
    parent_ids = indexes.MultiValueField()

    def get_model(self):
        return Folder

    def index_queryset(self, using=None):
        return self.get_model().objects.all().exclude(parent=None)

    def prepare(self, obj):
        data = super().prepare(obj)
        # data['suggestions'] = data['text']
        return data

    def prepare_parent_ids(self, obj):
        return _parent_ids(obj)


class DocumentIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(use_template=True, document=True)
    datetime = indexes.DateTimeField(model_attr="data__datetime")
    parent_ids = indexes.MultiValueField()
    suggestions = indexes.FacetCharField()

    def get_model(self):
        return Document

    def index_queryset(self, using=None):
        return self.get_model().objects.all().exclude(parent=None)

    def prepare_parent_ids(self, obj):
        return _parent_ids(obj)

    def prepare(self, obj):
        data = super().prepare(obj)
        file_obj = obj.data.file
        extracted_data = self.get_backend().extract_file_contents(file_obj)
        t = loader.select_template(('search/indexes/documents/document_text.txt',))
        data['text'] = t.render(Context({'object': obj, 'extracted': extracted_data}))
        # data['suggestions'] = data['text'][:30000]

        return data
