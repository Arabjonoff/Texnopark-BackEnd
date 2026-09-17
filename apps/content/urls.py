from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import EquipmentViewSet, FeatureViewSet, PartnerViewSet, SiteSettingsView, StatisticViewSet

router = DefaultRouter()
router.register('statistics', StatisticViewSet, basename='statistic')
router.register('features', FeatureViewSet, basename='feature')
router.register('equipment', EquipmentViewSet, basename='equipment')
router.register('partners', PartnerViewSet, basename='partner')

urlpatterns = [
    path('site-settings/', SiteSettingsView.as_view(), name='site-settings'),
    *router.urls,
]
