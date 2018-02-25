from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _

from ripa_archive.issues.forms import CreateIssueForm, IssueItemForm
from ripa_archive.issues.models import Issue, IssueItem
from ripa_archive.views import MultiFormView


ISSUES_ADD_MENU = (
    {"name": _("Issue"), "permalink": "!action:create-issue"},
)


def issues_base_context(request):
    return {
        "active_url_name": "issues",
        "add_menu": ISSUES_ADD_MENU
    }


def issues(request):
    context = issues_base_context(request)
    context.update({
        "items": Issue.objects.all(),
        "module_name": "issue",
        "title": _("Issues"),
        "edit_text": _("Edit issue"),
        "delete_text": _("Delete issue(s)"),
        "add_text": _("Add issue"),
    })
    return TemplateResponse(template="issues/list.html", request=request, context=context)


class CreateIssue(MultiFormView):
    title = _("Create issue")
    validator_url = "issues:validator-create-issue"
    form_class = IssueItemForm
    instance_class = IssueItem
    redirect_url_name = "issues:index"
    template = "issues/create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "main_data_form": CreateIssueForm(prefix="main")
        })
        return context

    def get(self, request, **kwargs):
        return super().get(request, **kwargs)
