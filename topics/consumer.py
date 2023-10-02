import json
from random import randint
from time import sleep
from channels.generic.websocket import AsyncWebsocketConsumer


class WSConsumer(AsyncWebsocketConsumer):
     async def connect(self):
          user_id = self.scope["user"].id
          await self.channel_layer.group_add(
            f"user_{user_id}", # Channel-Name der Gruppe mit UserId
            self.channel_name  # Der Name des WebSocket-Consumers
          )
          await self.accept()

     async def receive(self, text_data):
        pass

     async def disconnect(self, close_code):
        user_id = self.scope["user"].id
        
        # Den Client aus der Channel-Gruppe entfernen
        await self.channel_layer.group_discard(
            f"user_{user_id}",  # Channel-Name der Gruppe mit UserId
            self.channel_name  # Der Name des WebSocket-Consumers
        )

     async def send_data(self, event):
        data = event["data"]
        await self.send(json.dumps(data))