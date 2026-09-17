from django.http import Http404
from rest_framework import generics, mixins, viewsets

from .models import Equipment, Feature, Partner, SiteSettings, Statistic, TeamMember
from .serializers import (
    EquipmentSerializer,
    FeatureSerializer,
    PartnerSerializer,
    SiteSettingsSerializer,
    StatisticSerializer,
    TeamMemberSerializer,
)


class PublishedListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Faqat ro'yxat: saytda ko'rsatiladigan (is_published) yozuvlar, admin'dagi tartibda."""

    model = None
    pagination_class = None
    filter_backends = ()

    def get_queryset(self):
        return self.model.objects.filter(is_published=True)


class SiteSettingsView(generics.RetrieveAPIView):
    """Aloqa ma'lumotlari va ijtimoiy tarmoqlar (footer, aloqa sahifasi)."""

    serializer_class = SiteSettingsSerializer

    def get_object(self):
        settings = SiteSettings.load()
        if settings is None:
            raise Http404
        return settings


class StatisticViewSet(PublishedListViewSet):
    model = Statistic
    serializer_class = StatisticSerializer


class FeatureViewSet(PublishedListViewSet):
    model = Feature
    serializer_class = FeatureSerializer


class EquipmentViewSet(PublishedListViewSet):
    model = Equipment
    serializer_class = EquipmentSerializer


class TeamMemberViewSet(PublishedListViewSet):
    model = TeamMember
    serializer_class = TeamMemberSerializer


class PartnerViewSet(PublishedListViewSet):
    model = Partner
    serializer_class = PartnerSerializer
