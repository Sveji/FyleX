from django.urls import path
from document.consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/chatapp/', ChatConsumer.as_asgi()),
]