from ripa_archive.documents.models import Document
from ripa_archive.documents.strings import get_notification_text
from ripa_archive.issues.models import Issue
from ripa_archive.notifications.models import Notification, NotificationTranslation


def walk_by_followers(document, sender, create_notification_functor):
    for follower in document.followers.exclude(pk=sender.pk):
        create_notification_functor(follower)


def _create_translation(notification, title, detail):
    NotificationTranslation.objects.create(
        notification=notification,
        language_code="en",
        title=title,
        text=get_notification_text(detail, "en"),
    )

    NotificationTranslation.objects.create(
        notification=notification,
        language_code="ru",
        title=title,
        text=get_notification_text(detail, "ru"),
    )


def notification_remark(user, document, remark, detail, to_followers=False):
    def create_notification(to_user):
        notification = Notification.objects.create(
            user=user,
            to=to_user,
            content_type=Document.content_type,
            target_id=document.id,
            detail=remark.text
        )
        _create_translation(notification, str(document), detail)

    if to_followers:
        walk_by_followers(document, user, create_notification)

        if remark.user not in document.followers.all():
            create_notification(remark.user)
    else:
        create_notification(document.current_edit_meta.editor)


def notification_document(user, document, detail, to_followers=False):
    def create_notification(to_user):
        notification = Notification.objects.create(
            user=user,
            to=to_user,
            content_type=Document.content_type,
            target_id=document.id,
        )
        _create_translation(notification, str(document), detail)

    if to_followers:
        walk_by_followers(document, user, create_notification)
    else:
        create_notification(document.current_edit_meta.editor)


def notification_issue_remark(user, issue, remark, detail, to_followers=False):
    def create_notification(to_user):
        notification = Notification.objects.create(
            user=user,
            to=to_user,
            content_type=Issue.content_type,
            target_id=issue.id,
            detail=remark.text
        )
        _create_translation(notification, str(issue), detail)

    # parent = issue.owner.parent
    create_notification(issue.owner)

    # while parent is not None:
    #     create_notification(parent)
    #     parent = parent.parent
