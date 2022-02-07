import json

from rest_framework import status
from rest_framework.reverse import reverse

from houmers.tests.base import HoumBaseTestCase


class ReportsMoveTestCase(HoumBaseTestCase):

    def setUp(self):
        super().setUp()

    def _get_url(self):
        return reverse('houmers-reports-move')

    def _get_url_l(self):
        return reverse('houmers-location')

    def test_post_invalid_token(self):
        client = self.get_api_client(self.get_invalid_token())
        response = client.get(self._get_url())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        client = self.get_api_client(self.get_token_user())
        response = client.get(self._get_url())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_report(self):
        loc_a = (-34.587791, -58.422585)
        loc_b = (-34.591731, -58.432389)
        locations = [
            # 2 kmh
            {"latitude": loc_a[0], "longitude": loc_a[1], "altitude": 0, "date": "2022-01-31T00:00:00.999999Z"},
            {"latitude": loc_b[0], "longitude": loc_b[1], "altitude": 0, "date": "2022-01-31T00:30:00.999999Z"},
            {"latitude": loc_a[0], "longitude": loc_a[1], "altitude": 0, "date": "2022-01-31T01:00:00.999999Z"},
            {"latitude": loc_b[0], "longitude": loc_b[1], "altitude": 0, "date": "2022-01-31T01:30:00.999999Z"},
            {"latitude": loc_a[0], "longitude": loc_a[1], "altitude": 0, "date": "2022-01-31T02:00:00.999999Z"},
            # 1 kmh
            {"latitude": loc_b[0], "longitude": loc_b[1], "altitude": 0, "date": "2022-01-31T03:00:00.999999Z"},
            {"latitude": loc_a[0], "longitude": loc_a[1], "altitude": 0, "date": "2022-01-31T04:00:00.999999Z"},
            # 0 kmh
            {"latitude": loc_a[0], "longitude": loc_a[1], "altitude": 0, "date": "2022-01-31T04:00:00.999999Z"},
            {"latitude": loc_a[0], "longitude": loc_a[1], "altitude": 0, "date": "2022-01-31T04:00:00.999999Z"},
            # 4 kmh
            {"latitude": loc_b[0], "longitude": loc_b[1], "altitude": 0, "date": "2022-01-31T04:15:00.999999Z"},
            {"latitude": loc_a[0], "longitude": loc_a[1], "altitude": 0, "date": "2022-01-31T04:30:00.999999Z"},
        ]

        client = self.get_api_client(self.get_token_user())
        for loc in locations:
            response = client.post(self._get_url_l(), loc, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        client = self.get_api_client(self.get_token_admin())
        response = client.get(self._get_url() + f'?user={self.user.username}&date=2022-01-31&speed=1.5')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        j_response = json.loads(response.content)
        self.assertEqual(len(j_response), 2)

        j_response = [(m['date_from'], m['date_to']) for m in j_response]
        self.assertIn(("2022-01-31T00:00:00.999999Z", "2022-01-31T02:00:00.999999Z"), j_response)
        self.assertIn(("2022-01-31T04:00:00.999999Z", "2022-01-31T04:30:00.999999Z"), j_response)
