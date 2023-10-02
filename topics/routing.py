from django.urls import path
from .consumer import WSConsumer

ws_urlpatterns = [
    path("ws/data/", WSConsumer.as_asgi())
]