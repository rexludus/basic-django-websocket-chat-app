import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import WebSocket
from django.utils.crypto import get_random_string
from channels.db import database_sync_to_async

@database_sync_to_async
def write_websocket_credentials(token, room_name):
    WebSocket.objects.create(
        token = token,
        room_name = room_name,
    )

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """make first connection with the every client"""
        # extracting information from the routing.py
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # create token
        token = get_random_string(length=32)

        #TODO
        # add token and room_name to the db
        #write_websocket_credentials(token, self.room_name)

        # join clients to the same group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        # accept the get request and make handshake
        await self.accept()

        # send credentials (token and room_name) to browser
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_credentials_to_browser',
                'room_name': self.room_name,
                'token': token
            }
        )


    async def send_credentials_to_browser(self, event):
        room_name = event['room_name']
        token = event['token']
        await self.send(text_data=json.dumps({
            'room_name': room_name,
            'token': token,
        }))


    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )


    async def receive(self, text_data):
        """Handle incoming websocket data"""

        # coming from the browser
        text_data_json = json.loads(text_data)
        data_location = text_data_json['data_location']

        if(data_location == 'browser'):
            message = text_data_json['message']
            
            await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chatroom_message',
                'message': message,
            }
        )

        # getting user data from mobile 
        if(data_location == 'mobile'):
            user = text_data_json['user']

            print("user is: %s" % user)

            await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'mobile_handler',
                'user': user,
            }
        )


    async def chatroom_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message,
        }))

    async def mobile_handler(self, event):
        print("inside of mobile handler")
        user = event['user']

        await self.send(text_data=json.dumps({
            'user': user,
        }))    