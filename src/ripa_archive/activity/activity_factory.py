from django.core.exceptions import SuspiciousOperation

from ripa_archive.activity.models import Activity
from ripa_archive.documents import strings
from ripa_archive.documents.models import Document, Folder
from ripa_archive.notifications import notifications_factory


def _destruct_ref(ref):
    ref_id = None
    ref_content_type = ""
    ref_text = ""

    if ref is not None:
        if "instance" in ref:
            ref_id = ref["instance"].pk
            ref_content_type = ref["instance"].content_type
        else:
            ref_id = ref["id"]
            ref_content_type = ref["content_type"]

        ref_text = ref["text"]

    return ref_id, ref_content_type, ref_text


def for_document(user, document, detail, document_data=None, ref=None):
    ref_id, ref_content_type, ref_text = _destruct_ref(ref)
    Activity._factory_objects.create(
        user=user,
        content_type=Document.content_type,
        document_data=document_data,
        target_id=document.pk,
        details=detail,
        document_edit_meta=document.current_edit_meta,
        ref_id=ref_id,
        ref_text=ref_text,
        ref_content_type=ref_content_type,
    )
    notifications_factory.notification_document(user, document, detail, to_followers=True)


def for_folder(user, folder, detail, ref=None):
    ref_id, ref_content_type, ref_text = _destruct_ref(ref)
    Activity._factory_objects.create(
        user=user,
        content_type=Folder.content_type,
        target_id=folder.pk,
        details=detail,
        ref_id=ref_id,
        ref_text=ref_text,
        ref_content_type=ref_content_type,
    )


def delete(request, item):
    if isinstance(item, Folder):
        for_folder(
            request.user,
            item,
            strings.ACTIVITY_DELETE_FOLDER.format(path=item.path)
        )
    elif isinstance(item, Document):
        for_document(
            request.user,
            item,
            strings.ACTIVITY_DELETE_DOCUMENT.format(path=item.path)
        )
    else:
        raise SuspiciousOperation()


def move(request, old_path, item):
    if isinstance(item, Folder):
        for_folder(
            request.user,
            item,
            strings.ACTIVITY_MOVE_FOLDER.format(
                old_path=old_path,
                new_path=item.path
            )
        )
    elif isinstance(item, Document):
        for_document(
            request.user,
            item,
            strings.ACTIVITY_MOVE_DOCUMENT.format(
                old_path=old_path,
                new_path=item.path
            )
        )
    else:
        raise SuspiciousOperation()
