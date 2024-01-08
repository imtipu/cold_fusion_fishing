"""
URL configuration for cold_fusion_fishing project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from .utils.admin import html_image_logo
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

urlpatterns = [
                  path('', include('home.urls', namespace='home')),
                  path('admin/', admin.site.urls),
                  path('dashboard/', include('dashboard.urls', namespace='dashboard')),
                  path('accounts/', include('allauth.urls')),
                  path('accounts/', include('users.accounts.urls')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = html_image_logo()
admin.site.site_title = "Cold Fusion Admin"
admin.site.index_title = "Cold Fusion Admin Panel"

schema_view = get_schema_view(
   openapi.Info(
      title="Cold Fusion API",
      default_version='v1',
      description="Cold Fusion API Documentation",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="support@coldfusionbd.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.IsAdminUser,],
)

if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]

urlpatterns += [
    path('api/', include('api_modules.urls', namespace='api')),
    path('api-docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
