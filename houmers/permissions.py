from django.conf import settings
from django.contrib.auth.models import Group
from rest_framework.permissions import BasePermission

from houmers.models import HoumerUser


class IsAdminHoumer(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        admin_group, _ = Group.objects.get_or_create(name=settings.ADMIN_GROUP_NAME)
        user = HoumerUser.objects.get(pk=request.user.pk)
        return user.groups.all().filter(id=admin_group.id).exists()
