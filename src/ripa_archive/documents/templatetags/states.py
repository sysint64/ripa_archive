from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def folder_extra_classes(context, folder):
    request = context["request"]

    if folder.id in request.session.get("cut_folders", []):
        return " cut"

    return ""


@register.simple_tag(takes_context=True)
def document_extra_classes(context, document):
    request = context["request"]

    if document.id in request.session.get("cut_documents", []):
        return " cut"

    return ""
