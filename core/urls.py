from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path(f'api/{settings.API_VERSION}/', include('houmers.urls')),
]
