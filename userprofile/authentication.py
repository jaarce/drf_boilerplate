from django.core.exceptions import ObjectDoesNotExist
from rest_framework import authentication
from rest_framework.authtoken.models import Token


class AccessTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        access_token = request.GET.get('access_token')
        if access_token:
            try:
                token = Token.objects.get(key=access_token)
            except ObjectDoesNotExist:
                return None
        else:
            return None

        return token.user, None