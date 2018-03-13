from django.core.exceptions import SuspiciousOperation
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.utils.translation import ugettext_lazy as _

from request_helper import get_request_int_or_404
from ripa_archive.documents.views.forms import EditPermissions
from ripa_archive.issues.forms import IssueItemForm, CreateIssueWithOwnerForm, CreateIssueForm
from ripa_archive.issues.models import IssueItem
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
