from django.urls import path

from houmers.views import StatusView, LocationView, ReportsMoveView, PropertyList, PropertyDetail, ReportsVisitView

urlpatterns = [
    path('status', StatusView.as_view(), name='houmers-status'),
    path('location', LocationView.as_view(), name='houmers-location'),
    path('properties', PropertyList.as_view(), name='houmers-properties-list'),
    path('properties/<int:pk>', PropertyDetail.as_view(), name='houmers-properties-detail'),
    path('reports/visit', ReportsVisitView.as_view(), name='houmers-reports-visit'),
    path('reports/move', ReportsMoveView.as_view(), name='houmers-reports-move'),
]
