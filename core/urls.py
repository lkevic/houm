from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path('auth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path(f'api/{settings.API_VERSION}/', include('houmers.urls')),
]
