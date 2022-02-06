from django.http import Http404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from houmers.models import Property
from houmers.permissions import IsAdminHoumer
from houmers.serializers import LocationSerializer, TimeIntervalSerializer, ReportsMoveParams, PropertySerializer, \
    ReportsVisitParams, VisitSerializer
from houmers.services import ReportsService


class HoumersBaseView(APIView):
    permission_classes = [permissions.IsAuthenticated]


class HoumersAdminBaseView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminHoumer]


class StatusView(HoumersBaseView):

    @swagger_auto_schema(
        operation_description='Get the service status',
        responses={
            status.HTTP_200_OK: 'Ok',
        })
    def get(self, request, format=None):
        return Response({'service': 'Houmers', 'status': 'Ok'})


class LocationView(HoumersBaseView):

    @swagger_auto_schema(
        operation_description='Insert Location',
        request_body=LocationSerializer(),
        responses={
            status.HTTP_201_CREATED: 'Ok',
        })
    def post(self, request, format=None):
        serializer = LocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PropertyList(HoumersAdminBaseView):

    @swagger_auto_schema(
        operation_description='List all the properties',
        responses={
            status.HTTP_200_OK: PropertySerializer(many=True)
        }
    )
    def get(self, request, format=None):
        properties = Property.objects.filter()
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description='Create a new property',
        request_body=PropertySerializer(),
        responses={
            status.HTTP_201_CREATED: PropertySerializer(),
        })
    def post(self, request, format=None):
        serializer = PropertySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=self.request.user, modified_by=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PropertyDetail(HoumersAdminBaseView):

    def _get_object(self, pk):
        try:
            return Property.objects.get(pk=pk)
        except Property.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        operation_description='Get property',
        responses={
            status.HTTP_200_OK: PropertySerializer(),
        })
    def get(self, request, pk, format=None):
        prop = self._get_object(pk)
        serializer = PropertySerializer(prop)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description='Update property',
        request_body=PropertySerializer(),
        responses={
            status.HTTP_200_OK: PropertySerializer(),
        })
    def put(self, request, pk, format=None):
        prop = self._get_object(pk)
        serializer = PropertySerializer(prop, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(modified_by=self.request.user)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description='Delete property',
        responses={
            status.HTTP_204_NO_CONTENT: 'The property has been successfully removed',
        })
    def delete(self, request, pk, format=None):
        prop = self._get_object(pk)
        prop.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReportsMoveView(HoumersAdminBaseView):

    @swagger_auto_schema(
        operation_description='List all times where the Houmer moved faster than the specified speed',
        manual_parameters=[
            openapi.Parameter(
                name="user",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description="Houmer username"),
            openapi.Parameter(
                name="date",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description="Date of report. Format 'YYYY-MM-DD'"),
            openapi.Parameter(
                name="speed",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_NUMBER,
                required=True,
                description="Minimum speed"),
        ],
        responses={
            status.HTTP_200_OK: TimeIntervalSerializer(many=True)
        }
    )
    def get(self, request, format=None):
        s_params = ReportsMoveParams(data=self.request.query_params)
        s_params.is_valid(raise_exception=True)
        s_result = ReportsService().get_move_intervals(s_params)
        return Response(s_result.data, status=status.HTTP_200_OK)


class ReportsVisitView(HoumersAdminBaseView):

    @swagger_auto_schema(
        operation_description='List all the properties the Houmer has visited',
        manual_parameters=[
            openapi.Parameter(
                name="user",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description="Houmer username"),
            openapi.Parameter(
                name="date",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description="Date of report. Format 'YYYY-MM-DD'")
        ],
        responses={
            status.HTTP_200_OK: VisitSerializer(many=True)
        }
    )
    def get(self, request, format=None):
        s_params = ReportsVisitParams(data=self.request.query_params)
        s_params.is_valid(raise_exception=True)
        s_result = ReportsService().get_visits(s_params)
        return Response(s_result.data, status=status.HTTP_200_OK)
