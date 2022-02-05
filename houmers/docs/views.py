from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.conf import settings


schema_view = get_schema_view(
   openapi.Info(
      title="Houmer Service",
      default_version=settings.API_VERSION,
      description="Houm - Backend Tech Lead Challenge",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
