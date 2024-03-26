"""
ASGI config for chat_room project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from app.routing import websocket_urls
from channels.auth import AuthMiddlewareStack,AuthMiddleware
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_room.settings')

application = ProtocolTypeRouter(
    {
        'http':get_asgi_application(),
        'websocket':AuthMiddlewareStack(
            URLRouter(websocket_urls)
        )
    }
)