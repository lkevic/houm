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

    def handle(self, *args, **options):

        username = options["user"]
        password = options["password"]

        if HoumerUser.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR('Username already exist'))
            return

        HoumerUser.objects.create_user(username=username, password=password, is_active=True, is_admin=False)

        self.stdout.write(self.style.SUCCESS(f'User "{username}" was created'))
