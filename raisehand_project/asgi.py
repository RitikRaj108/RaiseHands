"""
ASGI config for RaiseHand Lite project.

ASGI (Asynchronous Server Gateway Interface) is the successor to WSGI.
It allows Django to handle:
- Traditional HTTP requests
- WebSocket connections
- Long-lived connections

This file configures the ProtocolTypeRouter to route:
- "http" traffic → Django's standard ASGI app
- "websocket" traffic → Django Channels with our custom routing

Interview Tip: 
"We use ASGI because WebSockets require persistent connections. 
WSGI only handles request-response cycles, but ASGI can handle 
long-lived connections needed for real-time features."
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'raisehand_project.settings')

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing any application modules
django_asgi_app = get_asgi_application()

# Import WebSocket routing AFTER Django is set up
from classroom.routing import websocket_urlpatterns

# ProtocolTypeRouter routes different protocols to different applications
# AuthMiddlewareStack adds session-based authentication to WebSocket
application = ProtocolTypeRouter({
    # HTTP requests are handled by Django's traditional ASGI application
    "http": django_asgi_app,
    
    # WebSocket connections are handled by our classroom routing
    # AuthMiddlewareStack allows us to access request.user in consumers
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
