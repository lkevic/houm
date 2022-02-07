import datetime

from django.conf import settings
from django.contrib.auth.models import Group
from django.utils import timezone
from django.test import TestCase
from oauth2_provider.models import Application
from oauth2_provider.oauth2_validators import AccessToken
from rest_framework.test import APIClient

from houmers.models import HoumerUser


class HoumBaseTestCase(TestCase):

    def setUp(self):

        self.admin_user = HoumerUser.objects.create_user(
            username='admin', password='Password123', is_active=True)
        admin_group, _ = Group.objects.get_or_create(name=settings.ADMIN_GROUP_NAME)
        self.admin_user.groups.add(admin_group)

        self.user = HoumerUser.objects.create_user(
            username='noadmin', password='Password456', is_active=True)

        self.cli_app = Application(
            client_id='123456',
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
            client_secret='123456',
        )
        self.cli_app.save()

        self.admin_token = AccessToken(
            user=self.admin_user,
            token='abcdef123456-admin-user',
            application=self.cli_app,
            expires=timezone.now() + datetime.timedelta(days=1),
            scope=''
        )
        self.admin_token.save()

        self.no_admin_token = AccessToken(
            user=self.user,
            token='abcdef123456-user',
            application=self.cli_app,
            expires=timezone.now() + datetime.timedelta(days=1),
            scope=''
        )
        self.no_admin_token.save()

    def get_token_admin(self):
        return self.admin_token.token

    def get_token_user(self):
        return self.no_admin_token.token

    def get_invalid_token(self):
        return '123456789-no-valid'

    def get_api_client(self, user_access_token: str) -> APIClient:
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_access_token}')
        return client
