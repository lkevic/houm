import json

from rest_framework import status
from rest_framework.reverse import reverse

from houmers.tests.base import HoumBaseTestCase


class PropertiesTestCase(HoumBaseTestCase):

    def setUp(self):
        super().setUp()

    def _get_url(self, pk=None):
        if not pk:
            return reverse('houmers-properties-list')
        else:
            return reverse('houmers-properties-detail', kwargs={'pk': pk})

    def test_post_invalid_token(self):
        client = self.get_api_client(self.get_invalid_token())
        response = client.post(self._get_url(), {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        client = self.get_api_client(self.get_token_user())
        response = client.post(self._get_url(), {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_property_crud(self):
        client = self.get_api_client(self.get_token_admin())
        response = client.get(self._get_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = client.post(self._get_url(), {"latitude": 0, "longitude": 0, "tolerance_radius": 20}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        pk = json.loads(response.content)['id']
        response = client.put(self._get_url(pk), {"latitude": 1, "longitude": 1, "tolerance_radius": 5}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = client.get(self._get_url(pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = client.delete(self._get_url(pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = client.get(self._get_url(pk))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_property_400(self):
        client = self.get_api_client(self.get_token_admin())
        response = client.post(self._get_url(), {"longitude": 0, "tolerance_radius": 20}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        client = self.get_api_client(self.get_token_admin())
        response = client.post(self._get_url(), {"latitude": 0, "tolerance_radius": 20}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        client = self.get_api_client(self.get_token_admin())
        response = client.post(self._get_url(), {"latitude": 0, "longitude": 0, "tolerance_radius": 20}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        pk = json.loads(response.content)['id']
        response = client.put(self._get_url(pk), {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
