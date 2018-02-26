from django.core.management import BaseCommand
from django.db import transaction

from ripa_archive.accounts.models import User
from ripa_archive.permissions.models import Group, Permission


class Command(BaseCommand):
    help = 'Create admin user'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)

    def handle(self, *args, **options):
        with transaction.atomic():
            admin_group, group_created = Group.objects.get_or_create(name="Admin")

            if group_created:
                for permission in Permission.objects.all():
                    admin_group.permissions.add(permission)

                admin_group.save()

            user = User.objects.create_user(options["email"], options["password"])
            user.group = admin_group
            user.save()

            self.stdout.write(self.style.SUCCESS('Successfully created user "%s"' % user.id))
