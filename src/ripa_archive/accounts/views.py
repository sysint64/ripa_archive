from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView
from django.contrib.auth import login
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ripa_archive.accounts.forms import LoginForm, UserForm
from ripa_archive.accounts.input_serializers import BulkInputSerializer
from ripa_archive.accounts.models import User
from ripa_archive.activity.models import Activity
from ripa_archive.documents.models import Document, DocumentEditMeta
from ripa_archive.permissions import codes
from ripa_archive.permissions.decorators import require_permissions


class LoginView(TemplateView):
    template_name = "login.html"

    def get_context_data(self, **kwargs):
        form = LoginForm(data=self.request.POST)

        context = super().get_context_data(**kwargs)
        context.update({"form": form})

        return context

    def post(self, request):
        form = LoginForm(data=self.request.POST)

        if not form.is_valid():
            print(form.errors)
            return self.get(request)

        login(request, form.user)
        return redirect(request.GET.get("next", "/"))


# Users --------------------------------------------------------------------------------------------


USERS_ADD_MENU = (
    {"name": "User", "permalink": "!action:create-user"},
)


def users_base_context(request):
    return {
        "active_url_name": "users",
        "add_menu": USERS_ADD_MENU
    }


@transaction.atomic
@require_permissions([codes.USERS_CAN_READ_PROFILE])
def users(request):
    context = users_base_context(request)
    context.update({
        "items": User.objects.all(),
        "module_name": "user",
        "title": "Users"
    })
    return TemplateResponse(template="users/list.html", request=request, context=context)


@transaction.atomic
@require_permissions([codes.USERS_CAN_READ_PROFILE])
def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)

    context = users_base_context(request)
    context.update({
        "items": User.objects.all(),
        "module_name": "user",
        "title": "Users",
        "profile_user": user,
        "recent_activity": Activity.objects.filter(user=user)[:5],
        "worked_on_documents_edit_metas": DocumentEditMeta.objects.filter(editor=user).order_by("-end_datetime")
    })
    return TemplateResponse(template="users/profile.html", request=request, context=context)


@require_http_methods(["GET", "POST"])
@transaction.atomic
@require_permissions([codes.USERS_CAN_CREATE])
def create(request):
    form = UserForm(request.POST, request.FILES)
    context = users_base_context(request)
    context.update({
        "form_title": "Create user",
        "form": form,
        "submit_title": "Create",
        "validator_url": reverse("accounts:validator-create"),
    })

    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.set_password("123321")  # TODO: send email with generated password
        user.save()

        messages.success(request, "Success added")
        return redirect("accounts:index")

    return TemplateResponse(template="forms/form.html", request=request, context=context)


@require_http_methods(["GET", "POST"])
@transaction.atomic
@require_permissions([codes.USERS_CAN_EDIT])
def update(request, user_id):
    instance = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=instance)
    else:
        form = UserForm(instance=instance)

    context = users_base_context(request)
    context.update({
        "form_title": "Update user",
        "form": form,
        "submit_title": "Update",
        "validator_url": reverse("accounts:validator-update", kwargs={"id": user_id}),
    })

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Success added")
        return redirect("accounts:index")

    return TemplateResponse(template="forms/form.html", request=request, context=context)


@api_view(["POST"])
@transaction.atomic
@require_permissions([codes.USERS_CAN_DELETE])
def delete(request):
    serializer = BulkInputSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    users = serializer.validated_data["users"]

    with transaction.atomic():
        for user in users:
            user.delete()

    return Response({}, status=status.HTTP_200_OK)
