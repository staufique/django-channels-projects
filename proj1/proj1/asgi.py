
import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter,URLRouter
from app.routing import websocket_urls
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj1.settings')

application = ProtocolTypeRouter(
    {
        'http':get_asgi_application(),
        'websocket':URLRouter(
            websocket_urls
        )
    }
)
