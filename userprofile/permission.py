from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions
from rest_framework.authtoken.models import Token


class AccessTokenPermission(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    message = 'Access Token is required'

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        access_token = request.GET.get('access_token')
        if access_token:
            try:
                Token.objects.get(key=access_token)
            except ObjectDoesNotExist:
                return False
            return True
        return False
