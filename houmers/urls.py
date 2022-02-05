from django.urls import path

from houmers.views import StatusView


urlpatterns = [
    path('status/', StatusView.as_view(), name='houmers-status'),
]
