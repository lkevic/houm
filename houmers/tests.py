from datetime import datetime, timedelta

from django.test import TestCase

from houmers.helpers import GISHelper


class GISHelperTestCase(TestCase):

    def setUp(self):
        self._now = datetime.now()
        self._five_minutes_from_now = self._now + timedelta(minutes=5)
        self._one_hour_from_now = self._now + timedelta(hours=1)
        self._two_hours_from_now = self._now + timedelta(hours=2)

    def test_distance_geodesic_WGS_84_ellipsoid(self):
        expected_distance = 19959.6792674 * 1000
        calculated_distance = GISHelper.calculate_distance_mts(
            p1_latitude=-41.32,
            p1_longitude=174.81,
            p1_altitude=None,
            p2_latitude=40.96,
            p2_longitude=-5.50,
            p2_altitude=None,
        )
        # Less than one meter error
        self.assertTrue(abs(expected_distance - calculated_distance) < 1)

    def test_distance_short_distance(self):
        expected_distance = 1 * 1000
        calculated_distance = GISHelper.calculate_distance_mts(
            p1_latitude=-34.587791,
            p1_longitude=-58.422585,
            p1_altitude=None,
            p2_latitude=-34.591731,
            p2_longitude=-58.432389,
            p2_altitude=None,
        )
        # Less than one meter error
        self.assertTrue(abs(expected_distance - calculated_distance) < 1)

    def test_distance_short_distance_with_altitude(self):
        expected_distance = 1.41421356237 * 1000
        calculated_distance = GISHelper.calculate_distance_mts(
            p1_latitude=-34.587791,
            p1_longitude=-58.422585,
            p1_altitude=0,
            p2_latitude=-34.591731,
            p2_longitude=-58.432389,
            p2_altitude=1000,
        )
        # Less than one meter error
        self.assertTrue(abs(expected_distance - calculated_distance) < 1)

    def test_speed(self):
        expected_speed = 19959.6792674
        calculated_speed = GISHelper.calculate_speed_kph(
            p1_latitude=-41.32,
            p1_longitude=174.81,
            p1_altitude=0,
            p1_datetime=self._now,
            p2_latitude=40.96,
            p2_longitude=-5.50,
            p2_altitude=0,
            p2_datetime=self._one_hour_from_now,
        )
        # Less than one kilometer per hour error
        self.assertTrue(abs(expected_speed - calculated_speed) < 1)

    def test_speed_short_distance(self):
        expected_speed = 1 / (5 / 60)
        calculated_speed = GISHelper.calculate_speed_kph(
            p1_latitude=-34.587791,
            p1_longitude=-58.422585,
            p1_altitude=0,
            p1_datetime=self._now,
            p2_latitude=-34.591731,
            p2_longitude=-58.432389,
            p2_altitude=0,
            p2_datetime=self._five_minutes_from_now,
        )
        self.assertTrue(abs(expected_speed - calculated_speed) < 0.01)

    def test_speed_short_distance_low_speed(self):
        expected_speed = 0.5
        calculated_speed = GISHelper.calculate_speed_kph(
            p1_latitude=-34.587791,
            p1_longitude=-58.422585,
            p1_altitude=0,
            p1_datetime=self._now,
            p2_latitude=-34.591731,
            p2_longitude=-58.432389,
            p2_altitude=0,
            p2_datetime=self._two_hours_from_now,
        )
        self.assertTrue(abs(expected_speed - calculated_speed) < 0.01)
