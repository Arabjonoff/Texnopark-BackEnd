from rest_framework import mixins, viewsets
from rest_framework.throttling import ScopedRateThrottle

from .serializers import ApplicationSerializer


class ApplicationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Saytdagi formalar: kursga yozilish, tadbirga ro'yxat, aloqa. Faqat yaratish (POST).

    Spamga qarshi IP bo'yicha cheklov bor (settings: DEFAULT_THROTTLE_RATES['applications']).
    Next.js server action so'rovni yuborganda foydalanuvchi IP'sini X-Forwarded-For orqali uzatadi.
    """

    serializer_class = ApplicationSerializer
    throttle_classes = (ScopedRateThrottle,)
    throttle_scope = 'applications'
