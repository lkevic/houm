import math
from datetime import datetime
from typing import Union

from geopy import distance
from houmers.models import HoumerUser


class HoumerOAuth2TokenManager(object):
    @staticmethod
    def revoke_all_user_tokens(user: HoumerUser):
        if hasattr(user, 'oauth2_provider_accesstoken'):
            user.oauth2_provider_accesstoken.all().delete()
        if hasattr(user, 'oauth2_provider_refreshtoken'):
            user.oauth2_provider_refreshtoken.all().delete()


class GISHelper(object):

    _DISTANCE_ERROR_MTS = 0.001

    @staticmethod
    def calculate_distance_mts(
            p1_latitude: float,
            p1_longitude: float,
            p1_altitude: Union[None, float],
            p2_latitude: float,
            p2_longitude: float,
            p2_altitude: Union[None, float],
    ) -> float:
        flat_distance = distance.distance((p1_latitude, p1_longitude), (p2_latitude, p2_longitude)).meters
        if p1_altitude is not None \
                and p2_altitude is not None \
                and abs(p1_altitude - p2_altitude) > GISHelper._DISTANCE_ERROR_MTS:
            return math.sqrt(flat_distance**2 + (p1_altitude - p2_altitude)**2)
        return flat_distance

    @staticmethod
    def calculate_speed_kph(
            p1_latitude: float,
            p1_longitude: float,
            p1_altitude: Union[None, float],
            p1_datetime: datetime,
            p2_latitude: float,
            p2_longitude: float,
            p2_altitude: Union[None, float],
            p2_datetime: datetime,
    ) -> float:
        total_seconds = abs((p2_datetime - p1_datetime).total_seconds())
        if total_seconds == 0:
            return 0
        p_distance = GISHelper.calculate_distance_mts(
            p1_latitude=p1_latitude,
            p1_longitude=p1_longitude,
            p1_altitude=p1_altitude,
            p2_latitude=p2_latitude,
            p2_longitude=p2_longitude,
            p2_altitude=p2_altitude,
        )
        return (p_distance / 1000) / (total_seconds / 60 / 60)
