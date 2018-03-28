from django.contrib import messages
from django.core.exceptions import SuspiciousOperation, PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.utils.translation import ugettext_lazy as _

from request_helper import get_request_int_or_404
from ripa_archive.documents import strings
from ripa_archive.documents.views.forms import EditPermissions
from ripa_archive.issues.forms import IssueItemForm, CreateIssueWithOwnerForm, CreateIssueForm, \
    RemarkForm
from ripa_archive.issues.models import IssueItem, Issue, Remark
from ripa_archive.issues.views.main import issues_base_context
from ripa_archive.notifications import notifications_factory
from ripa_archive.permissions import codes
from ripa_archive.permissions.decorators import require_permissions
from ripa_archive.views import MultiFormView


class CreateIssue(MultiFormView):
    title = _("Create issue")
    validator_url = "issues:validator-create-issue"
    form_class = IssueItemForm
    instance_class = IssueItem
    redirect_url_name = "issues:index"
    template = "issues/create.html"

    def get_context_data(self, **kwargs):
        form = CreateIssueWithOwnerForm(prefix="main")
        context = super().get_context_data(**kwargs)
        context.update({
            "main_data_form": form,
            "submit_title": _("Create issue"),
            "add_title": _("Add another item")
        })
        return context

    def get(self, request, **kwargs):
        return super().get(request, **kwargs)

    @transaction.atomic
    def post(self, request, **kwargs):
        set_auto_owner = False
        form = CreateIssueWithOwnerForm(prefix="main", data=request.POST)

        if not form.is_valid():
            raise SuspiciousOperation()

        self.issue = form.save(commit=False)

        if set_auto_owner:
            self.issue.owner = request.user

        self.issue.save()

        return super().post(request, **kwargs)

    def perform_save(self, form):
        item = form.save(commit=False)
        item.issue = self.issue
        item.save()


# TODO: reduce repetition
class UpdateIssue(EditPermissions):
    title = _("Update issue")
    validator_url = "issues:validator-create-issue"
    form_class = IssueItemForm
    instance_class = IssueItem
    redirect_url_name = "issues:index"
    template = "issues/create.html"
    instance = None

    def get_for_instance(self, **kwargs):
        return self.get_instance_or_404(kwargs["issue_id"])

    def get_instance_or_404(self, issue_id):
        if self.instance is None:
            self.instance = get_object_or_404(Issue, id=issue_id)

        return self.instance

    def get_queryset(self, for_instance):
        return self.instance_class.objects.filter(issue=for_instance)

    def get_context_data(self, **kwargs):
        instance = self.get_instance_or_404(kwargs["issue_id"])
        context = super().get_context_data(**kwargs)
        context.update({
            "main_data_form": CreateIssueForm(prefix="main", instance=instance),
            "submit_title": _("Update issue"),
            "add_title": _("Add another item")
        })
        return context

    def get(self, request, **kwargs):
        return super().get(request, **kwargs)

    @transaction.atomic
    def post(self, request, **kwargs):
        instance = self.get_instance_or_404(kwargs["issue_id"])
        form = CreateIssueForm(prefix="main", data=request.POST, instance=instance)

        if not form.is_valid():
            raise SuspiciousOperation()

        self.issue = form.save(commit=False)
        self.issue.owner = request.user
        self.issue.save()

        return super().post(request, **kwargs)

    def perform_save(self, form):
        item = form.save(commit=False)
        item.issue = self.issue
        item.save()


@require_http_methods(["GET", "POST"])
@transaction.atomic
# TODO: @require_permissions
def write_remark(request, issue_id, issue_item_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    issue_item = get_object_or_404(IssueItem, pk=issue_item_id, issue=issue)

    reject_remark_id = request.GET.get("reject_remark_id")
    remark_to_reject = None
    reject_issue_item = request.GET.get("reject")

    if reject_remark_id is not None:
        reject_remark_id = get_request_int_or_404(request, "GET", "reject_remark_id")
        remark_to_reject = get_object_or_404(Remark, id=reject_remark_id)

        if remark_to_reject.is_rejected:
            raise PermissionDenied()

    form = RemarkForm(request.POST)

    context = issues_base_context(request)
    context.update({
        "form_title": _("Write remark"),
        "form": form,
        "submit_title": _("Submit"),
        "validator_url": reverse("issues:validator-write-remark"),
    })

    if request.method == "POST" and form.is_valid():
        remark = form.save(commit=False)
        remark.issue_item = issue_item
        remark.user = request.user
        remark.save()

        if reject_issue_item is not None:
            remark_to_reject = remark
            issue_item.status = IssueItem.Status.IN_PROGRESS
            issue_item.save()

        # Reject remark
        if remark_to_reject is not None:
            remark_to_reject.status = Remark.Status.REJECTED
            remark_to_reject.save()

            notifications_factory.notification_issue_remark(
                request.user,
                issue,
                remark_to_reject,
                strings.NOTIFICATION_REMARK_REJECTED
            )

        notifications_factory.notification_issue_remark(
            request.user,
            issue,
            remark,
            strings.NOTIFICATION_REMARK_WROTE
        )

        messages.success(request, _("Successfully submitted remark"))
        return redirect(issue.permalink)

    return TemplateResponse(template="forms/form.html", request=request, context=context)
