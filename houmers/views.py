from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from houmers.serializers import LocationSerializer


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
