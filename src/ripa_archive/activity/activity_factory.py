from ripa_archive.activity.models import Activity
from ripa_archive.documents.models import Document, Folder
from ripa_archive.notifications import notifications_factory


def for_document(user, document, detail, document_data=None):
    Activity._factory_objects.create(
        user=user,
        content_type=Document.content_type,
        document_data=document_data,
        target_id=document.pk,
        details=detail,
        document_edit_meta=document.current_edit_meta
    )
    notifications_factory.notification_document(user, document, detail, to_followers=True)


def for_folder(user, folder, detail):
    Activity._factory_objects.create(
        user=user,
        content_type=Folder.content_type,
        target_id=folder.pk,
        details=detail
    )
