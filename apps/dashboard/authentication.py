from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication


def token_expires_at(token):
    return token.created + timedelta(hours=settings.DASHBOARD_TOKEN_TTL_HOURS)


class ExpiringTokenAuthentication(TokenAuthentication):
    """DRF token + amal qilish muddati. Muddati o'tgan token o'chiriladi — qayta login talab qilinadi."""

    def authenticate_credentials(self, key):
        user, token = super().authenticate_credentials(key)
        if timezone.now() >= token_expires_at(token):
            token.delete()
            raise exceptions.AuthenticationFailed('Sessiya muddati tugagan. Qaytadan kiring.')
        if not user.is_staff:
            raise exceptions.AuthenticationFailed("Dashboard'ga kirish huquqi yo'q.")
        return user, token
