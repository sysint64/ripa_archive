from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth import login

from ripa_archive.accounts.forms import LoginForm


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
