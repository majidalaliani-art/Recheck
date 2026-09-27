import json
from channels.generic.websocket import AsyncWebsocketConsumer


class GlobalConsumer(AsyncWebsocketConsumer):


    async def connect(self):
        self.group_name = "global"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
    async def global_update(self, event):

        await self.send(text_data=json.dumps(event["data"]))


class OrderConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        phone = self.scope["session"].get("user")
        
        self.group_name = f"client_{phone}"

        # self.order_id = self.scope["url_route"]["kwargs"]["order_id"]
        # self.group_name = f"order_{self.order_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
    async def client_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))
