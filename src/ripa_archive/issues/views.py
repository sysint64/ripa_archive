from django.core.exceptions import SuspiciousOperation
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ripa_archive.issues.input_serializers import BulkInputSerializer
from ripa_archive.documents.views.forms import EditPermissions
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


# TODO: Add permissions
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


# TODO: Add permissions
def issue(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    context = issues_base_context(request)
    context.update({
        "issue": issue,
        "title": issue.name
    })
    return TemplateResponse(template="issues/single.html", request=request, context=context)


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

    @transaction.atomic
    def post(self, request, **kwargs):
        form = CreateIssueForm(prefix="main", data=request.POST)

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
            "main_data_form": CreateIssueForm(prefix="main", instance=instance)
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


@api_view(["POST"])
def delete(request):
    serializer = BulkInputSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    issues = serializer.validated_data["issues"]

    with transaction.atomic():
        for issue in issues:
            issue.delete()

    return Response({}, status=status.HTTP_200_OK)
