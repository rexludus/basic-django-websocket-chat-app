from cgitb import text
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect


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
              #  'channel_name': self.channel_name,
            }
        )


    # 'type': 'tester_message',
    async def send_credentials(self, event):
        room_name = event['room_name']
        room_group_name = event['room_group_name']
       # channel_name = event['channel_name']
        await self.send(text_data=json.dumps({
            'room_name': room_name,
            'room_group_name': room_group_name,
           # 'channel_name': channel_name,
        }))


    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )


    async def receive(self, text_data):
        """Handle incoming websocket data"""

        """coming from the browser"""
        text_data_json = json.loads(text_data)
        data_location = text_data_json['data_location']
        message = text_data_json['message']
        user = text_data_json['user']

        if(data_location == 'browser'):
            await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chatroom_message',
                'message': message,
                'user': user,
            }
        )



    async def chatroom_message(self, event):
        message = event['message']
        user = event['user']

        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
        }))