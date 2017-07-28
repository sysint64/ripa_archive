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


def users(request):
    context = users_base_context(request)
    context.update({
        "items": User.objects.all(),
        "module_name": "user",
        "title": "Users"
    })
    return TemplateResponse(template="users/list.html", request=request, context=context)


@require_http_methods(["GET", "POST"])
@transaction.atomic
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
        form.save()
        messages.success(request, "Success added")
        return redirect("accounts:index")

    return TemplateResponse(template="forms/form.html", request=request, context=context)


@require_http_methods(["GET", "POST"])
@transaction.atomic
def update(request, email):
    instance = get_object_or_404(User, email=email)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=instance)
    else:
        form = UserForm(instance=instance)

    context = users_base_context(request)
    context.update({
        "form_title": "Update user",
        "form": form,
        "submit_title": "Update",
        "validator_url": reverse("accounts:validator-update", kwargs={"email": email}),
    })

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Success added")
        return redirect("accounts:index")

    return TemplateResponse(template="forms/form.html", request=request, context=context)


@api_view(["POST"])
def delete(request):
    serializer = BulkInputSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    users = serializer.validated_data["users"]

    with transaction.atomic():
        for user in users:
            user.delete()

    return Response({}, status=status.HTTP_200_OK)
