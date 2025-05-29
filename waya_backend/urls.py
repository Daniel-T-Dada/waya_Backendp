from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.http import JsonResponse

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
    path('users/', include('users.urls')),
    path('children/', include('children.urls')),
    path('taskmaster/', include('taskmaster.urls')),
]
