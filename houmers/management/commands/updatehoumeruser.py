from django.conf import settings
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from houmers.helpers import HoumerOAuth2TokenManager
from houmers.models import HoumerUser


class Command(BaseCommand):
    """
    Update Houmer user
    Example:
        manage.py updatehoumeruser --user=user123 --newpassword=Changeme123 --active True --admin False
    """

    def add_arguments(self, parser):

        parser.add_argument("--user", required=True)
        parser.add_argument("--newpassword", required=False)
        parser.add_argument("--active", required=False, choices=['False', 'True'])
        parser.add_argument("--admin", required=False, choices=['False', 'True'])

    def handle(self, *args, **options):

        username = options["user"]
        password = options["newpassword"]
        active = str(options["active"]) == 'True' if options["active"] is not None else None
        is_admin = str(options["admin"]) == 'True' if options["admin"] is not None else None

        try:
            user = HoumerUser.objects.get(username=username)
            if password is not None:
                user.set_password(password)
            if active is not None:
                user.is_active = active
                if not active:
                    HoumerOAuth2TokenManager.revoke_all_user_tokens(user)
            if is_admin is not None:
                admin_group, _ = Group.objects.get_or_create(name=settings.ADMIN_GROUP_NAME)
                if is_admin:
                    user.groups.add(admin_group)
                else:
                    user.groups.remove(admin_group)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'User "{username}" was updated'))

        except HoumerUser.DoesNotExist:
            self.stdout.write(self.style.ERROR('Username does not exist'))
