from django import template

register = template.Library()


@register.assignment_tag(takes_context=True)
def folder_has_permission(context, folder, permission):
    request = context["request"]
    return folder.is_user_has_permission(request.user, permission)


@register.assignment_tag(takes_context=True)
def document_has_permission(context, document, permission):
    request = context["request"]
    return document.is_user_has_permission(request.user, permission)
