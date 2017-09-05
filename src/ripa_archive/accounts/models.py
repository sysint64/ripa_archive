from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from ripa_archive.permissions.models import Group


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    class Gender:
        UNSET = '0'
        MALE = 'm'
        FEMALE = 'f'

        CHOICES = (
            (UNSET, _('Unset')),
            (MALE, _('Male')),
            (FEMALE, _('Female')),
        )

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    email = models.EmailField(unique=True)
    gender = models.CharField(
        verbose_name=_("Gender"),
        choices=Gender.CHOICES,
        default=Gender.UNSET,
        max_length=1,
    )

    avatar_image = models.ImageField(_("Avatar image"), blank=True)
    first_name = models.CharField(_("First name"), max_length=30, blank=True)
    last_name = models.CharField(_("Last name"), max_length=30, blank=True)
    group = models.ForeignKey(Group, null=True)

    location = models.CharField(_("Location"), max_length=255, blank=True)
    position = models.CharField(_("Position"), max_length=100, blank=True)
    web_site = models.URLField(_("Web site"), max_length=100, blank=True)

    is_active = models.BooleanField(
        _('Is active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('Date joined'), default=timezone.now)
    objects = UserManager()

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def __str__(self):
        if self.get_full_name().strip() == "":
            return self.email
        else:
            return self.get_full_name().strip()

    @property
    def ref(self):
        return self.id

    @property
    def permalink(self):
        return reverse("accounts:profile", kwargs={"user_id": self.id})

    @property
    def gender_icon(self):
        return {
            User.Gender.UNSET: "fa-genderless",
            User.Gender.MALE: "fa-mars",
            User.Gender.FEMALE: "fa-venus",
        }.get(self.gender)

    @property
    def gender_str(self):
        return {
            User.Gender.UNSET: _("Unset"),
            User.Gender.MALE: _("Male"),
            User.Gender.FEMALE: _("Female"),
        }.get(self.gender)

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)
