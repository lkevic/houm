from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response


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
