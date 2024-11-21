from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Setup for Swagger documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version='v1',
        description="API description for your Django project"
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/', include('users.urls')),  # URLs for user management (non-auth related actions)
    path('api/v1/store/', include('store.urls')),  # URLs for the store app
    
    # Add the auth app URLs
    path('api/auth/', include('custom_auth.urls')),  # Assuming `auth.urls` exists and handles new authentication routes

    # Re-path or re-assign JWT related paths if needed, or they might be already handled in 'auth.urls'
    # path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    # Swagger and Redoc URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),

    # path('accounts/', include("django.contrib.auth.urls")),
]

# Adding static and media URLs
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
