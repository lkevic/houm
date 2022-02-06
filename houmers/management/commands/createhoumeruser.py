from django.conf import settings
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from houmers.models import HoumerUser


class Command(BaseCommand):
    """
    Create Houmer user
    Example:
        manage.py createhoumeruser --user=user123 --password=Changeme123
    """

    def add_arguments(self, parser):
        parser.add_argument("--user", required=True)
        parser.add_argument("--password", required=True)
        parser.add_argument("--admin", required=False, choices=['False', 'True'])

    def handle(self, *args, **options):

        username = options["user"]
        password = options["password"]
        is_admin = str(options["admin"]) == 'True' if options["admin"] is not None else None

        if HoumerUser.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR('Username already exist'))
            return

        admin_group, _ = Group.objects.get_or_create(name=settings.ADMIN_GROUP_NAME)

        user = HoumerUser.objects.create_user(username=username, password=password, is_active=True, is_admin=False)

        if is_admin is not None:
            admin_group, _ = Group.objects.get_or_create(name=settings.ADMIN_GROUP_NAME)
            if is_admin:
                user.groups.add(admin_group)
            else:
                user.groups.remove(admin_group)
            user.save()

        self.stdout.write(self.style.SUCCESS(f'User "{username}" was created'))
