"""
WSGI config for RaiseHand Lite project.

Note: This project primarily uses ASGI for WebSocket support.
This WSGI configuration is kept for compatibility with traditional
WSGI servers if needed.

For running the server, use Daphne (ASGI) instead:
    daphne raisehand_project.asgi:application
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'raisehand_project.settings')

application = get_wsgi_application()
