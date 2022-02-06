from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from houmers.serializers import LocationSerializer, TimeIntervalSerializer, ReportsMoveParams
from houmers.services import ReportsService


class HoumersBaseView(APIView):
    permission_classes = [permissions.IsAuthenticated]


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


class ReportsMoveView(HoumersBaseView):

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
