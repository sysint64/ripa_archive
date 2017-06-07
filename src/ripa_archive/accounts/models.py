from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from easy_thumbnails.fields import ThumbnailerImageField


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
            (UNSET, 'Незадан'),
            (MALE, 'Мужской'),
            (FEMALE, 'Женский'),
        )

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    email = models.EmailField(unique=True)
    gender = models.CharField(
        verbose_name="gender",
        choices=Gender.CHOICES,
        default=Gender.UNSET,
        max_length=1,
    )

    avatar_image = ThumbnailerImageField(blank=True)
    first_name = models.CharField("first name", max_length=30, blank=True)
    last_name = models.CharField("last name", max_length=30, blank=True)

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)