# Engineer/routing.py
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    # path("ws/order/<int:order_id>/", consumers.OrderConsumer.as_asgi()),
    path("ws/orders/", consumers.OrderConsumer.as_asgi()),
    path("ws/global/", consumers.GlobalConsumer.as_asgi()),
]
