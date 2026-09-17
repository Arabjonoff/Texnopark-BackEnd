from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

admin.site.site_header = 'Andijon Yoshlar Texnoparki'
admin.site.site_title = 'Texnopark admin'
admin.site.index_title = 'Sayt kontentini boshqarish'

api_patterns = [
    path('', include('apps.courses.urls')),
    path('', include('apps.events.urls')),
    path('', include('apps.content.urls')),
    path('', include('apps.projects.urls')),
    path('', include('apps.news.urls')),
    path('', include('apps.applications.urls')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_patterns)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
