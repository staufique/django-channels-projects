"""
ASGI config for real_time_data_js project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from app.routing import websocket_urls


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'real_time_data_js.settings')

application = ProtocolTypeRouter(
    {
        'http':get_asgi_application(),
        'websocket':URLRouter(
            websocket_urls
        )
    }
)
