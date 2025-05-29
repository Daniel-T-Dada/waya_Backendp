from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

def redirect_root(request):  
    return redirect('/users')

def health_check(request):
    """Health check endpoint for Render deployment"""
    return JsonResponse({
        'status': 'healthy',
        'message': 'Waya Backend API is running'
    })

urlpatterns = [
    path('', redirect_root),
    path('health/', health_check, name='health-check'),
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # Authentication API Endpoints (prefixed with /api/)
    path('api/', include('users.api_urls')),
    
    # Other API Endpoints
    path('users/', include('users.urls')),
    path('children/', include('children.urls')),
    path('taskmaster/', include('taskmaster.urls')),
]
