from haystack import indexes
from ripa_archive.documents.models import Folder, Document


class FolderIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(model_attr="name", document=True)

    def get_model(self):
        return Folder

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class DocumentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(model_attr="name", document=True)
    owner = indexes.CharField(use_template=True)
    status = indexes.CharField(model_attr="status__name")
    datetime = indexes.DateTimeField(model_attr="data__datetime")

    def get_model(self):
        return Document

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
