from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.views.generic import TemplateView
from django.contrib.auth import login

from ripa_archive.accounts.forms import LoginForm
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
        "module_name": "users",
        "title": "Users"
    })
    return TemplateResponse(template="users/list.html", request=request, context=context)
