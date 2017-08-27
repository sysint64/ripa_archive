from django import template

register = template.Library()


@register.assignment_tag(takes_context=True)
def user_has_permission_for_instance(context, instance, permission):
    request = context["request"]
    return instance.is_user_has_permission(request.user, permission)


# @register.assignment_tag(takes_context=True)
# def document_has_permission(context, document, permission):
#     request = context["request"]
#     return document.is_user_has_permission(request.user, permission)

@register.assignment_tag(takes_context=True)
def user_has_permission(context, permission):
    request = context["request"]
    return request.user.group.has_permission(permission)
