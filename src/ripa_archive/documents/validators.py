from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

NAME_REGEX = "[0-9a-zA-ZА-Яа-я /\-]+"
NAME_MAX_LENGTH = 255

name_validator = RegexValidator(
    regex="^{}$".format(NAME_REGEX),
    message=_("Not allowed special characters")
)
