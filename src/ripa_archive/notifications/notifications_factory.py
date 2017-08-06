from ripa_archive.documents.models import Document
from ripa_archive.notifications.models import Notification


def walk_by_followers(document, sender, create_notification_functor):
    for follower in document.followers.exclude(pk=sender.pk):
        create_notification_functor(follower)


def notification_remark(user, document, remark, string, to_followers=False):
    def create_notification(to_user):
        Notification.objects.create(
            user=user,
            to=to_user,
            content_type=Document.content_type,
            target_id=document.id,
            title=str(document),
            text=string,
            detail=remark.text
        )

    if to_followers:
        walk_by_followers(document, user, create_notification)
    else:
        create_notification(document.current_edit_meta.editor)
