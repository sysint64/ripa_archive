from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _

from ripa_archive.accounts.models import User
from ripa_archive.issues.models import Issue

ISSUES_ADD_MENU = (
    {"name": _("Issue"), "permalink": "!action:create-issue"},
)


def issues_base_context(request):
    return {
        "active_url_name": "issues",
        "add_menu": ISSUES_ADD_MENU
    }


# TODO: Add permissions
@login_required(login_url="accounts:login")
def issues(request):
    issues = []

    def create_issue_payload(for_user):
        return {
            "owner": for_user,
            "issues": Issue.objects.active_issues().filter(owner=for_user),
            "children": []
        }

    def issues_tree_for_user(for_user):
        payload = create_issue_payload(for_user)

        for user in User.objects.filter(parent=for_user):
            payload["children"].append(issues_tree_for_user(user))

        return payload

    with transaction.atomic():
        issues.append(issues_tree_for_user(request.user))

    context = issues_base_context(request)
    context.update({
        "issues": issues,
        "module_name": "issue",
        "title": _("Issues"),
        "edit_text": _("Edit issue"),
        "delete_text": _("Delete issue(s)"),
        "add_text": _("Add issue"),
    })
    return TemplateResponse(template="issues/list.html", request=request, context=context)


# TODO: Add permissions
def issue(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    context = issues_base_context(request)
    context.update({
        "issue": issue,
        "title": issue.name,
        "reviewer": issue.owner.is_child_of(request.user)
    })
    return TemplateResponse(template="issues/single/index.html", request=request, context=context)
