from rest_framework.exceptions import ValidationError

from houmers.helpers import GISHelper
from houmers.models import Location, HoumerUser
from houmers.serializers import TimeIntervalSerializer, ReportsMoveParams


class ReportsService(object):

    def get_move_intervals(self, params_serializer: ReportsMoveParams) -> TimeIntervalSerializer:

        data = params_serializer.validated_data
        username: str = data['user']
        date_from: str = data['date'].strftime('%Y-%m-%d') + ' 00:00:00.000000'
        date_to: str = data['date'].strftime('%Y-%m-%d') + ' 23:59:59.999999'
        minimum_speed: float = data['speed']

        if not HoumerUser.objects.filter(username=username).exists():
            raise ValidationError("Invalid username")

        locations = Location.objects\
            .filter(user__username=username, date__range=[date_from, date_to])\
            .order_by('date')
        if len(locations) < 2:
            s_result = TimeIntervalSerializer(data=[], many=True)
            s_result.is_valid()
            return s_result
        locations = list(locations)

        result = []
        d_from = locations.pop(0)
        interval_from = None
        interval_to = None
        for location in locations:
            speed = GISHelper.calculate_speed_kph(
                p1_latitude=d_from.latitude,
                p1_longitude=d_from.longitude,
                p1_altitude=d_from.altitude,
                p1_datetime=d_from.date,
                p2_latitude=location.latitude,
                p2_longitude=location.longitude,
                p2_altitude=location.altitude,
                p2_datetime=location.date,
            )
            if speed > minimum_speed:
                if interval_from is None:
                    interval_from = d_from.date
                interval_to = location.date
            else:
                if interval_from is not None:
                    result.append({'date_from': interval_from, 'date_to': interval_to})
                interval_from = interval_to = None
            d_from = location

        if interval_from is not None:
            result.append({'date_from': interval_from, 'date_to': interval_to})

        s_result = TimeIntervalSerializer(data=result, many=True)
        s_result.is_valid()
        return s_result
