from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _

from ripa_archive.accounts.models import User
from ripa_archive.issues.models import Issue, IssueItem

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
    """
    TODO:
    Потом он сказал, что там где идет нумерация задач #1, #4 и т.д.
    это нужно убрать сделать фильтр вместо #1  должна быть маркировка по типу задач,
    Например красный и буква Б - безопасность, это надо придумать и продумать какую маркировку делать,
    чтобы потом можно было отфильтровывать и смотреть по типу задач
    """
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
        "add_text": _("Add issue")
    })
    return TemplateResponse(template="issues/list.html", request=request, context=context)


# TODO: Add permissions
def issue(request, issue_id):
    """
    Кнопка одобрить (Status.APPROVED) - доступна вышестоящему по иерархии,
    кнопка старт (Status.IN_PROGRESS) - нажимает юзер,
    кнопка пауза (Status.PAUSED) - может нажать и юзер и вышестоящий по иерархии,
    кнопка завершить (Status.FINISHED) - нажимает юзер и может если нужно нажать вышестоящий по иерархии,
    кнопка отклонить (Status.REJECTED) - нажимает вышестоящий по иерархии и
    кнопка утвердить (Status.CONFIRMED)- нажимает вышестоящий по иерархии
    """
    issue = get_object_or_404(Issue, id=issue_id)
    context = issues_base_context(request)

    is_user_superior_in_hierarchy = issue.owner.is_child_of(request.user)
    is_owner = request.user == issue.owner

    context.update({
        "issue": issue,
        "issue_items": IssueItem.objects.items_for_issue(issue),
        "title": issue.name,
        "reviewer": is_user_superior_in_hierarchy,
        "is_owner": is_owner,
        "displays_approve_button": is_user_superior_in_hierarchy,
        "displays_confirm_button": is_user_superior_in_hierarchy,
        "displays_start_button": is_owner,
        "displays_pause_button": is_owner or is_user_superior_in_hierarchy,
        "displays_finish_button": is_owner or is_user_superior_in_hierarchy,
        "displays_reject_button": is_user_superior_in_hierarchy,
        "displays_review_button": is_user_superior_in_hierarchy
    })
    return TemplateResponse(template="issues/single/index.html", request=request, context=context)
