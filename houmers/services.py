from rest_framework.exceptions import ValidationError

from houmers.helpers import GISHelper
from houmers.models import Location, HoumerUser, Property
from houmers.serializers import TimeIntervalSerializer, ReportsMoveParams, VisitSerializer, ReportsVisitParams


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

    def get_visits(self, params_serializer: ReportsVisitParams) -> VisitSerializer:

        data = params_serializer.validated_data
        username: str = data['user']
        date_from: str = data['date'].strftime('%Y-%m-%d') + ' 00:00:00.000000'
        date_to: str = data['date'].strftime('%Y-%m-%d') + ' 23:59:59.999999'

        if not HoumerUser.objects.filter(username=username).exists():
            raise ValidationError("Invalid username")

        locations = Location.objects\
            .filter(user__username=username, date__range=[date_from, date_to])\
            .order_by('date')
        if len(locations) < 1:
            s_result = VisitSerializer(data=[], many=True)
            s_result.is_valid()
            return s_result

        properties = list(Property.objects.all())
        if len(properties) < 1:
            s_result = VisitSerializer(data=[], many=True)
            s_result.is_valid()
            return s_result

        locations = list(locations)

        result = []
        interval_from = None
        interval_to = None
        actual_prop = None
        for location in locations:
            in_prop = False
            for prop in properties:
                dist = GISHelper.calculate_distance_mts(
                    p1_latitude=prop.latitude,
                    p1_longitude=prop.longitude,
                    p1_altitude=None,
                    p2_latitude=location.latitude,
                    p2_longitude=location.longitude,
                    p2_altitude=None,
                )
                if dist <= prop.tolerance_radius:
                    in_prop = True
                    if actual_prop is None:
                        actual_prop = prop
                        interval_from = location.date
                        interval_to = location.date
                    else:
                        if actual_prop.pk == prop.pk:
                            interval_to = location.date
                        else:
                            result.append({'prop': actual_prop, 'date_from': interval_from, 'date_to': interval_to})
                            actual_prop = prop
                            interval_from = location.date
                            interval_to = location.date
                    break
            if actual_prop is not None and not in_prop:
                result.append({'prop': actual_prop, 'date_from': interval_from, 'date_to': interval_to})
                actual_prop = interval_from = interval_to = None

        if actual_prop is not None:
            result.append({'prop': actual_prop, 'date_from': interval_from, 'date_to': interval_to})

        t_result = []
        for d in result:
            t_result.append({
                'duration': d['date_to'] - d['date_from'],
                'latitude': d['prop'].latitude,
                'longitude': d['prop'].longitude})
        s_result = VisitSerializer(data=t_result, many=True)
        s_result.is_valid()
        return s_result
