"""
URL configuration for RaiseHand Lite project.

Main URL router that includes all application URLs.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin interface (optional, for user management)
    path('admin/', admin.site.urls),
    
    # Classroom app URLs (student and teacher views)
    path('', include('classroom.urls')),
]
