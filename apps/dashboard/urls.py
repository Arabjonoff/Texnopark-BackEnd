from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter(trailing_slash=True)
router.include_root_view = False
router.register('courses', views.CourseViewSet, basename='dashboard-course')
router.register('events', views.EventViewSet, basename='dashboard-event')
router.register('news', views.PostViewSet, basename='dashboard-news')
router.register('statistics', views.StatisticViewSet, basename='dashboard-statistic')
router.register('features', views.FeatureViewSet, basename='dashboard-feature')
router.register('equipment', views.EquipmentViewSet, basename='dashboard-equipment')
router.register('partners', views.PartnerViewSet, basename='dashboard-partner')
router.register('video-stories', views.VideoStoryViewSet, basename='dashboard-video-story')
router.register('applications', views.ApplicationViewSet, basename='dashboard-application')

urlpatterns = [
    path('auth/login/', views.LoginView.as_view(), name='dashboard-login'),
    path('auth/logout/', views.LogoutView.as_view(), name='dashboard-logout'),
    path('auth/me/', views.MeView.as_view(), name='dashboard-me'),
    path('stats/', views.StatsView.as_view(), name='dashboard-stats'),
    path('site-settings/', views.SiteSettingsView.as_view(), name='dashboard-site-settings'),
    *router.urls,
]
