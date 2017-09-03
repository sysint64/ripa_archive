from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.utils.translation import ugettext_lazy as _

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ripa_archive.permissions import codes
from ripa_archive.permissions.decorators import require_permissions, require_at_least_one_permission
from ripa_archive.permissions.forms import GroupForm
from ripa_archive.permissions.input_serializers import BulkInputSerializer
from ripa_archive.permissions.models import Group


PERMISSIONS_ADD_MENU = (
    {"name": _("Group"), "permalink": "!action:create-group"},
)


def permissions_base_context(request):
    return {
        "active_url_name": "permissions",
        "add_menu": PERMISSIONS_ADD_MENU
    }


@login_required(login_url="accounts:login")
@transaction.atomic
@require_at_least_one_permission([codes.GROUPS_CAN_CREATE, codes.GROUPS_CAN_EDIT, codes.GROUPS_CAN_DELETE])
def permissions(request):
    context = permissions_base_context(request)
    context.update({
        "items": Group.objects.all(),
        "module_name": "group",
        "title": _("User groups")
    })
    return TemplateResponse(template="groups.html", request=request, context=context)


@require_http_methods(["GET", "POST"])
@transaction.atomic
@require_permissions([codes.GROUPS_CAN_CREATE])
def create_group(request):
    form = GroupForm(request.POST)

    context = permissions_base_context(request)
    context.update({
        "form_title": _("Create group"),
        "form": form,
        "submit_title": _("Create"),
        "validator_url": reverse("permissions:validator-create"),
    })

    if request.method == "POST" and form.is_valid():
        group = form.save()
        group.permissions = form.permissions
        group.save()

        messages.success(request, _("Success added"))
        return redirect("permissions:index")

    return TemplateResponse(template="forms/form.html", request=request, context=context)


@require_http_methods(["GET", "POST"])
@transaction.atomic
@require_permissions([codes.GROUPS_CAN_EDIT])
def update_group(request, name):
    instance = get_object_or_404(Group, name=name)

    if request.method == "POST":
        form = GroupForm(request.POST, instance=instance)
    else:
        form = GroupForm(
            instance=instance,
            initial=GroupForm.initial(instance)
        )

    context = permissions_base_context(request)
    context.update({
        "form_title": _("Update group"),
        "form": form,
        "submit_title": _("Update"),
        "validator_url": reverse("permissions:validator-update", kwargs={"name": name}),
    })

    if request.method == "POST" and form.is_valid():
        group = form.save(commit=False)
        group.permissions = form.permissions
        group.save()

        messages.success(request, _("Success added"))
        return redirect("permissions:index")

    return TemplateResponse(template="forms/form.html", request=request, context=context)


@api_view(["POST"])
@transaction.atomic
@require_permissions([codes.GROUPS_CAN_DELETE])
def delete_group(request):
    serializer = BulkInputSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    groups = serializer.validated_data["groups"]

    with transaction.atomic():
        for group in groups:
            group.delete()

    return Response({}, status=status.HTTP_200_OK)
