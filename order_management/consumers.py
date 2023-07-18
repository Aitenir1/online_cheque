from channels.generic.websocket import AsyncWebsocketConsumer
import json


class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            "model_instances",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def send_model_instance(self, event):
        instance = event['instance']
        await self.send(text_data=instance)
