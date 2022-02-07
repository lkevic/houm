from rest_framework import status
from rest_framework.reverse import reverse

from houmers.tests.base import HoumBaseTestCase


class LocationTestCase(HoumBaseTestCase):

    def setUp(self):
        super().setUp()

    def _get_url(self):
        return reverse('houmers-location')

    def test_post_invalid_token(self):
        client = self.get_api_client(self.get_invalid_token())
        response = client.post(self._get_url(), {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_400(self):
        client = self.get_api_client(self.get_token_user())
        response = client.post(self._get_url(), {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = client.post(self._get_url(),
                               {"latitude": 0, "longitude": 0, "altitude": 0, "date": "xxxxxxxx"},
                               format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = client.post(self._get_url(),
                               {"latitude": 0, "longitude": 0, "altitude": 9999999, "date": "2022-02-06T22:24:21.969Z"},
                               format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = client.post(self._get_url(),
                               {"latitude": 200.0, "longitude": 0, "altitude": 0, "date": "2022-02-06T22:24:21.969Z"},
                               format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = client.post(self._get_url(),
                               {"latitude": 0, "longitude": 200.0, "altitude": 0, "date": "2022-02-06T22:24:21.969Z"},
                               format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_200(self):
        client = self.get_api_client(self.get_token_user())
        response = client.post(self._get_url(),
                               {"latitude": 0, "longitude": 0, "altitude": 0, "date": "2022-02-06T22:24:21.969Z"},
                               format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
