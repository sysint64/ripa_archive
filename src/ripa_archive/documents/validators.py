from django.core.validators import RegexValidator

NAME_REGEX = "[0-9a-zA-ZА-Яа-я /\-]+"
NAME_MAX_LENGTH = 255

name_validator = RegexValidator(
    regex="^{}$".format(NAME_REGEX),
    message="Not allowed special characters"
)
