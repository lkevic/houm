from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response


class HoumersBaseView(APIView):
    permission_classes = [permissions.IsAuthenticated]


class StatusView(HoumersBaseView):

    def get(self, request, format=None):
        return Response({'service': 'Houmers', 'status': 'Ok'})
