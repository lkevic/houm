from django.urls import path

from houmers.views import StatusView, LocationView

urlpatterns = [
    path('status', StatusView.as_view(), name='houmers-status'),
    path('location', LocationView.as_view(), name='houmers-location'),
    
]
