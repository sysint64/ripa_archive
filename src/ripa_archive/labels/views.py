from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.template.response import TemplateResponse
from django.contrib import messages
from django.views.decorators.http import require_http_methods

from ripa_archive.labels.forms import LabelForm
from ripa_archive.labels.models import Label

LABELS_ADD_MENU = (
    {"name": _("Label"), "permalink": "!action:create-label"},
)


def labels_base_context(request):
    return {
        "active_url_name": "labels",
        "add_menu": LABELS_ADD_MENU
    }


def labels(request):
    context = labels_base_context(request)
    context.update({
        "items": Label.objects.all(),
        "module_name": "label",
        "title": _("Label"),
        "edit_text": _("Edit label"),
        "delete_text": _("Delete label(s)"),
        "add_text": _("Add label")
    })
    return TemplateResponse(template="labels/list.html", request=request, context=context)


@require_http_methods(["GET", "POST"])
def create(request):
    form = LabelForm(request.POST)
    context = labels_base_context(request)
    context.update({
        "form_title": _("Create label"),
        "form": form,
        "submit_title": _("Create"),
        "validator_url": reverse("labels:validator-create"),
    })

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, _("Success added"))
        return redirect("labels:index")

    return TemplateResponse(template="forms/form.html", request=request, context=context)


@require_http_methods(["GET", "POST"])
def update(request, label_id):
    instance = get_object_or_404(Label, id=label_id)

    if request.method == "POST":
        form = LabelForm(request.POST, request.FILES, instance=instance)
    else:
        form = LabelForm(instance=instance)

    context = labels_base_context(request)
    context.update({
        "form_title": _("Update label"),
        "form": form,
        "submit_title": _("Update"),
        "validator_url": reverse("labels:validator-update", kwargs={"id": label_id}),
    })

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, _("Success updated"))
        return redirect("labels:index")

    return TemplateResponse(template="forms/form.html", request=request, context=context)
