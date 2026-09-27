import json
from channels.generic.websocket import AsyncWebsocketConsumer


class UserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope.get("user")
        if not self.user or not self.user.is_authenticated:
            await self.close()
            return

        self.room_name = f"user_{self.user.id}"
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "room_name"):
            await self.channel_layer.group_discard(
                self.room_name, self.channel_name
            )

    # --------------------------------------------------
    # الأحداث المعالجة داخل الغرفة (Event Handlers)
    # --------------------------------------------------

    # 1. حدث تحديث المحفظة
    async def wallet_update(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "action": "wallet_update",
                    "wallet": event.get("wallet", {}),  
                }
            )
        )

    # 2. حدث تحديث الطلبات
    async def order_update(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "action": "order_update",
                    "data": event.get("data", {}),
                }
            )
        )
