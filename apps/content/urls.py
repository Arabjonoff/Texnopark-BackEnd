from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    EquipmentViewSet,
    FeatureViewSet,
    PartnerViewSet,
    SiteSettingsView,
    StatisticViewSet,
    TeamMemberViewSet,
)

router = DefaultRouter()
router.register('statistics', StatisticViewSet, basename='statistic')
router.register('features', FeatureViewSet, basename='feature')
router.register('equipment', EquipmentViewSet, basename='equipment')
router.register('partners', PartnerViewSet, basename='partner')
router.register('team', TeamMemberViewSet, basename='team-member')

urlpatterns = [
    path('site-settings/', SiteSettingsView.as_view(), name='site-settings'),
    *router.urls,
]
