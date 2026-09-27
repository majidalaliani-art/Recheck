# Engineer/routing.py
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/user/", consumers.UserConsumer.as_asgi()),

]
