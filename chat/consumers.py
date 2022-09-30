import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # extracting information from the routing.py
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_credentials',
                'room_name': self.room_name,
                'room_group_name': self.room_group_name,
                'channel_name': self.channel_name,
            }
        )


    # 'type': 'tester_message',
    async def send_credentials(self, event):
        room_name = event['room_name']
        room_group_name = event['room_group_name']
        channel_name = event['channel_name']
        await self.send(text_data=json.dumps({
            'room_name': room_name,
            'room_group_name': room_group_name,
            'channel_name': channel_name,
        }))


    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chatroom_message',
                'message': message,
            }
        )


    async def chatroom_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message,
        }))