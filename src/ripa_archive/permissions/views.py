from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from ripa_archive.permissions.forms import CreateGroupForm
from ripa_archive.permissions.models import Group

PERMISSIONS_ADD_MENU = (
    {"name": "Group", "permalink": "!action:create-group"},
)


def permissions_base_context(request):
    return {
        "active_url_name": "permissions",
        "add_menu": PERMISSIONS_ADD_MENU
    }


@login_required(login_url="accounts:login")
def permissions(request):
    context = permissions_base_context(request)
    context.update({
        "items": Group.objects.all(),
        "module_name": "group",
        "title": "User groups"
    })
    return TemplateResponse(template="module_list.html", request=request, context=context)


@require_http_methods(["GET", "POST"])
@transaction.atomic
def create_group(request):
    form = CreateGroupForm(request.POST)

    context = permissions_base_context(request)
    context.update({
        "form_title": "Create group",
        "form": form,
        "submit_title": "Create",
        "validator_url": reverse("permissions:validator-create-group"),
    })

    if request.method == "POST" and form.is_valid():
        group = form.save()
        group.permissions = form.permissions
        group.save()

        messages.success(request, "Success added")
        return redirect("permissions:index")

    return TemplateResponse(template="forms/form.html", request=request, context=context)


@require_http_methods(["GET", "POST"])
@transaction.atomic
def update_group(request, name):
    instance = get_object_or_404(Group, name=name)

    if request.method == "POST":
        form = CreateGroupForm(request.POST, instance=instance)
    else:
        form = CreateGroupForm(
            instance=instance,
            initial={
                "folder_permissions": instance.permissions.all(),
                "documents_permissions": instance.permissions.all()
            }
        )

    context = permissions_base_context(request)
    context.update({
        "form_title": "Update group",
        "form": form,
        "submit_title": "Update",
        "validator_url": reverse("permissions:validator-update-group", kwargs={"name": name}),
    })

    if request.method == "POST" and form.is_valid():
        group = form.save(commit=False)
        group.permissions = form.permissions
        group.save()

        messages.success(request, "Success added")
        return redirect("permissions:index")

    return TemplateResponse(template="forms/form.html", request=request, context=context)
