import json

from rest_framework import status
from rest_framework.reverse import reverse

from houmers.tests.base import HoumBaseTestCase


class ReportsVisitTestCase(HoumBaseTestCase):

    def setUp(self):
        super().setUp()

    def _get_url(self):
        return reverse('houmers-reports-visit')

    def _get_url_l(self):
        return reverse('houmers-location')

    def _get_url_p(self):
        return reverse('houmers-properties-list')

    def test_post_invalid_token(self):
        client = self.get_api_client(self.get_invalid_token())
        response = client.get(self._get_url())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        client = self.get_api_client(self.get_token_user())
        response = client.get(self._get_url())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_report(self):

        loc_a_0 = (-34.587791, -58.422585)
        loc_a_1 = (-34.587782, -58.422586)
        loc_a_2 = (-34.587798, -58.422581)

        loc_b_0 = (-34.591731, -58.432389)
        loc_b_1 = (-34.591740, -58.432380)
        loc_b_2 = (-34.591722, -58.432395)

        loc_c_0 = (-34.902511, -58.985635)
        loc_c_1 = (-34.902500, -58.985640)

        loc_d_0 = (-32.102501, -57.085699)

        loc_e_0 = (-31.102501, -54.085699)
        loc_f_0 = (-33.102501, -58.085699)

        locations = [
            {"latitude": loc_d_0[0], "longitude": loc_d_0[1], "altitude": 0, "date": "2022-01-31T00:00:00.000000Z"},
            {"latitude": loc_a_2[0], "longitude": loc_a_2[1], "altitude": 0, "date": "2022-01-31T00:30:00.000000Z"},
            {"latitude": loc_a_1[0], "longitude": loc_a_1[1], "altitude": 0, "date": "2022-01-31T01:00:00.000000Z"},
            {"latitude": loc_a_2[0], "longitude": loc_a_2[1], "altitude": 0, "date": "2022-01-31T01:30:00.000000Z"},
            {"latitude": loc_a_2[0], "longitude": loc_a_2[1], "altitude": 0, "date": "2022-01-31T02:00:00.000000Z"},
            {"latitude": loc_b_1[0], "longitude": loc_b_1[1], "altitude": 0, "date": "2022-01-31T03:00:00.000000Z"},
            {"latitude": loc_b_2[0], "longitude": loc_b_2[1], "altitude": 0, "date": "2022-01-31T04:00:00.000000Z"},
            {"latitude": loc_d_0[0], "longitude": loc_d_0[1], "altitude": 0, "date": "2022-01-31T04:00:00.000000Z"},
            {"latitude": loc_d_0[0], "longitude": loc_d_0[1], "altitude": 0, "date": "2022-01-31T04:00:00.000000Z"},
            {"latitude": loc_c_1[0], "longitude": loc_c_1[1], "altitude": 0, "date": "2022-01-31T04:15:00.000000Z"},
            {"latitude": loc_d_0[0], "longitude": loc_d_0[1], "altitude": 0, "date": "2022-01-31T04:30:00.000000Z"},
        ]

        client = self.get_api_client(self.get_token_user())
        for loc in locations:
            response = client.post(self._get_url_l(), loc, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        properties = [
            {"latitude": loc_e_0[0], "longitude": loc_e_0[1], "tolerance_radius": 30},
            {"latitude": loc_a_0[0], "longitude": loc_a_0[1], "tolerance_radius": 25},
            {"latitude": loc_b_0[0], "longitude": loc_b_0[1], "tolerance_radius": 20},
            {"latitude": loc_c_0[0], "longitude": loc_c_0[1], "tolerance_radius": 30},
            {"latitude": loc_f_0[0], "longitude": loc_f_0[1], "tolerance_radius": 25},
        ]

        client = self.get_api_client(self.get_token_admin())
        for prop in properties:
            response = client.post(self._get_url_p(), prop, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.get(self._get_url() + f'?user={self.user.username}&date=2022-01-31')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        j_response = json.loads(response.content)
        self.assertEqual(len(j_response), 3)
        self.assertIn({'duration': "01:30:00", 'latitude': loc_a_0[0], 'longitude': loc_a_0[1]}, j_response)
        self.assertIn({'duration': "01:00:00", 'latitude': loc_b_0[0], 'longitude': loc_b_0[1]}, j_response)
        self.assertIn({'duration': "00:00:00", 'latitude': loc_c_0[0], 'longitude': loc_c_0[1]}, j_response)
