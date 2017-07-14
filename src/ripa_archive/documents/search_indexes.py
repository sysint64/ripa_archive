from django.template import Context
from django.template import loader
from haystack import indexes
from ripa_archive.documents.models import Folder, Document


class FolderIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(model_attr="name", document=True)
    parent_id = indexes.FacetCharField(model_attr="parent__id")

    def get_model(self):
        return Folder

    def index_queryset(self, using=None):
        return self.get_model().objects.all().exclude(parent=None)


class DocumentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(use_template=True, document=True)
    datetime = indexes.DateTimeField(model_attr="data__datetime")
    parent_id = indexes.FacetCharField(model_attr="parent__id")

    def get_model(self):
        return Document

    def index_queryset(self, using=None):
        return self.get_model().objects.all().exclude(parent=None)

    def prepare(self, obj):
        data = super().prepare(obj)
        file_obj = obj.data.file
        extracted_data = self.get_backend().extract_file_contents(file_obj)
        t = loader.select_template(('search/indexes/documents/document_text.txt',))
        data['text'] = t.render(Context({'object': obj, 'extracted': extracted_data}))

        return data
