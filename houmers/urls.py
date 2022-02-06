from django.urls import path

from houmers.views import StatusView, LocationView, ReportsMoveView

urlpatterns = [
    path('status', StatusView.as_view(), name='houmers-status'),
    path('location', LocationView.as_view(), name='houmers-location'),
    path('reports/move', ReportsMoveView.as_view(), name='houmers-reports-move'),
]
