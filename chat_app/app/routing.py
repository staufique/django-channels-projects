from django.urls import path
from .consumers import *


websocket_urls=[
    path("ws/sc/",MySyncConsumer.as_asgi()),
    path("ws/ac/",MyASyncConsumer.as_asgi())
]