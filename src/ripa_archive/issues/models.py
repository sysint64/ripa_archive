from django.db import models, transaction
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from ripa_archive.accounts.models import User
from ripa_archive.documents.validators import NAME_MAX_LENGTH
from ripa_archive.labels.models import Label


class IssuesManager(models.Manager):
    def active_issues(self):
        return super().get_queryset().filter(is_active=True)


class Issue(models.Model):
    content_type = "issues.Issue"
    owner = models.ForeignKey(User, related_name="issue_owner")
    datetime = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=60)
    is_active = models.BooleanField(default=True)

    objects = IssuesManager()

    def __str__(self):
        return self.name

    @property
    def labels(self):
        labels = []

        for item in IssueItem.objects.items_for_issue(self):
            labels.extend(item.labels.all())

        print(labels)
        return labels

    @property
    def ref(self):
        return self.id

    @property
    def permalink(self):
        return reverse("issues:single", kwargs={"issue_id": self.id})

    @property
    @transaction.atomic
    def fullness_percents(self):
        # NOTE: Этот запрос наверное можно переписать с использованием аггрегаций
        # и получить прирост в производительности.
        total = self.issueitem_set.count()
        finished_count = self.issueitem_set.filter(status=IssueItem.Status.FINISHED).count()
        approved_count = self.issueitem_set.filter(is_approved=True).count()
        confirmed_count = self.issueitem_set.filter(status=IssueItem.Status.CONFIRMED).count()

        return {
            "finished": (finished_count + confirmed_count) / total * 100,
            "approved": approved_count / total * 100,
            "confirmed": confirmed_count / total * 100,
        }

    @property
    def is_approved(self):
        return int(self.fullness_percents["approved"]) == 100

    @property
    def is_finished(self):
        return int(self.fullness_percents["finished"]) == 100

    @property
    def is_confirmed(self):
        return int(self.fullness_percents["confirmed"]) == 100

    def css_class(self):
        if self.is_approved:
            return " approved"
        elif self.is_finished:
            return " finished"
        else:
            return ""


class IssueItemManager(models.Manager):
    def items_for_issue(self, issue):
        items = []

        for item in super().get_queryset().filter(issue=issue):
            items.append(item)

        issues1 = super().get_queryset().filter(issue__is_active=True, users=issue.owner)

        for issue in issues1:
            items.append(issue)

        return items


class IssueItem(models.Model):
    class Status:
        OPEN = "0"
        IN_PROGRESS = "1"
        FINISHED = "2"
        REJECTED = "3"
        CONFIRMED = "4"

        CHOICES = (
            (OPEN, _("Open")),
            (IN_PROGRESS, _("In progress")),
            (FINISHED, _("Finished")),
            (CONFIRMED, _("Confirmed")),
            (REJECTED, _("Rejected")),
        )

    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    name = models.CharField(max_length=NAME_MAX_LENGTH, default="No name")
    content = models.TextField()
    status = models.CharField(max_length=1, default=Status.OPEN)
    users = models.ManyToManyField(User)
    labels = models.ManyToManyField(Label)
    is_paused = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    objects = IssueItemManager()

    @property
    def is_open(self):
        return self.status == IssueItem.Status.OPEN

    @property
    def is_in_progress(self):
        return self.status == IssueItem.Status.IN_PROGRESS

    @property
    def is_finished(self):
        return self.status == IssueItem.Status.FINISHED

    @property
    def is_confirmed(self):
        return self.status == IssueItem.Status.CONFIRMED

    @property
    def is_rejected(self):
        return self.status == IssueItem.Status.REJECTED

    @property
    def css_class(self):
        return {
            IssueItem.Status.OPEN: " open",
            IssueItem.Status.IN_PROGRESS: " in-progress",
            IssueItem.Status.FINISHED: " finished",
            IssueItem.Status.REJECTED: " rejected",
            IssueItem.Status.CONFIRMED: " approved",
        }.get(self.status, "")

    @property
    def status_name(self):
        return {
            IssueItem.Status.OPEN: "Открыт",
            IssueItem.Status.IN_PROGRESS: "В работе",
            IssueItem.Status.FINISHED: "Завершен",
            IssueItem.Status.REJECTED: "Отклонен",
            IssueItem.Status.CONFIRMED: "Утвержден",
        }.get(self.status, "")


class InProgressRemarkManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(issue_item__status=IssueItem.Status.IN_PROGRESS)


# TODO: Можно вынести в абстрактную модель
class Remark(models.Model):
    class Status:
        ACTIVE = '0'
        ACCEPTED = '1'
        REJECTED = '2'
        FINISHED = '3'

    class Meta:
        ordering = ["-datetime"]

    issue_item = models.ForeignKey(IssueItem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="issues_remark_user")
    text = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, default=Status.ACTIVE)

    objects = models.Manager()
    in_progress_objects = InProgressRemarkManager()

    @property
    def is_accepted(self):
        return self.status == Remark.Status.ACCEPTED

    @property
    def is_rejected(self):
        return self.status == Remark.Status.REJECTED

    @property
    def is_finished(self):
        return self.status == Remark.Status.FINISHED

    @property
    def is_active(self):
        return self.status == Remark.Status.ACTIVE

    @property
    def css_class(self):
        return {
            Remark.Status.ACCEPTED: " accepted",
            Remark.Status.REJECTED: " rejected",
            Remark.Status.FINISHED: " finished",
        }.get(self.status, "")
