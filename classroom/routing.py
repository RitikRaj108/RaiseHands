"""
WebSocket URL Routing for RaiseHand Lite

This module defines URL patterns for WebSocket connections,
similar to how urls.py defines HTTP routes.

URL Pattern: ws/classroom/<room_name>/
- room_name: Unique identifier for the classroom session
- Students and teachers connect to the same room to interact
"""

from django.urls import re_path
from . import consumers

# WebSocket URL patterns
# These are handled by ASGI, not WSGI
websocket_urlpatterns = [
    # Route WebSocket connections to ClassroomConsumer
    # Example: ws://localhost:8000/ws/classroom/room1/
    re_path(
        r'ws/classroom/(?P<room_name>\w+)/$',
        consumers.ClassroomConsumer.as_asgi()
    ),
]
