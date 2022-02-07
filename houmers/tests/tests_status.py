from rest_framework import status
from rest_framework.reverse import reverse

from houmers.tests.base import HoumBaseTestCase


class StatusTestCase(HoumBaseTestCase):

    def setUp(self):
        super().setUp()

    def _get_url(self):
        return reverse('houmers-status')

    def test_get_status_invalid_token(self):
        client = self.get_api_client(self.get_invalid_token())
        response = client.get(self._get_url())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_status(self):
        client = self.get_api_client(self.get_token_admin())
        response = client.get(self._get_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
