from django import template

from ripa_archive.permissions import codes

register = template.Library()


@register.assignment_tag(takes_context=True)
def user_has_permission_for_instance(context, instance, permission):
    request = context["request"]
    return instance.is_user_has_permission(request.user, permission)


@register.assignment_tag(takes_context=True)
def html_document_data_perms(context, document):
    request = context["request"]
    can_edit = document.is_user_has_permission(request.user, codes.DOCUMENTS_CAN_EDIT)
    can_delete = document.is_user_has_permission(request.user, codes.DOCUMENTS_CAN_DELETE)
    can_edit_permissions = document.is_user_has_permission(request.user, codes.DOCUMENTS_CAN_EDIT_PERMISSIONS)

    return "edit:{};delete:{};edit_permissions:{}".format(
        "1" if can_edit else "0",
        "1" if can_delete else "0",
        "1" if can_edit_permissions else "0",
    )


@register.assignment_tag(takes_context=True)
def html_folder_data_perms(context, folder):
    request = context["request"]
    can_edit = folder.is_user_has_permission(request.user, codes.FOLDERS_CAN_EDIT)
    can_delete = folder.is_user_has_permission(request.user, codes.FOLDERS_CAN_DELETE)
    can_edit_permissions = folder.is_user_has_permission(request.user, codes.FOLDERS_CAN_EDIT_PERMISSIONS)
    can_create_documents = folder.is_user_has_permission(request.user, codes.DOCUMENTS_CAN_CREATE)
    can_create_folders = folder.is_user_has_permission(request.user, codes.FOLDERS_CAN_CREATE)

    return "edit:{};delete:{};edit_permissions:{};create_documents:{};create_folders:{}".format(
        "1" if can_edit else "0",
        "1" if can_delete else "0",
        "1" if can_edit_permissions else "0",
        "1" if can_create_documents else "0",
        "1" if can_create_folders else "0",
    )


@register.assignment_tag(takes_context=True)
def user_has_permission(context, permission):
    request = context["request"]
    return request.user.group.has_permission(permission)
