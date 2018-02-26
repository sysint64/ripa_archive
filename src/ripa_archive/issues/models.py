from django.db import models
from django.urls import reverse

from ripa_archive.accounts.models import User
from ripa_archive.documents.validators import NAME_MAX_LENGTH


class Issue(models.Model):
    owner = models.ForeignKey(User, related_name="issue_owner")
    name = models.CharField(max_length=NAME_MAX_LENGTH, default="No name")
    followers = models.ManyToManyField(User, related_name="issue_followers")

    @property
    def ref(self):
        return self.id

    @property
    def permalink(self):
        return reverse("issues:single", kwargs={"issue_id": self.id})


class IssueItem(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    name = models.CharField(max_length=NAME_MAX_LENGTH, default="No name")
    content = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)

    # json field with different statues
    statuses = models.TextField()
