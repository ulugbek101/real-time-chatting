import json
from datetime import timedelta

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.db.models import Q, QuerySet

from .models import Message

User = get_user_model()
rooms = {}

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['username'].replace("@", "")
        self.user = self.scope['user']
        self.room_group_name = f'chat_room_{''.join(sorted([self.user.username, self.room_name]))}'

        if self.room_group_name not in rooms:
            rooms[self.room_group_name] = set()
        rooms[self.room_group_name].add(self.channel_name)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        print(rooms)
        await self.accept()

        # Send the quantity of people in room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'people_in_chat_quantity',
                'data': {
                    'type': 'people_in_chat_quantity',
                    'count': len(rooms[self.room_group_name]) - 1,
                }
            }
        )

        # Send existing messages to the newly connected user
        message_history = await self.get_message_history()
        await self.send_message_history(message_history)


    async def disconnect(self, code):
        # Remove the channel from the room's channel list
        if self.channel_name in rooms[self.room_group_name]:
            rooms[self.room_group_name].discard(self.channel_name)

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # If no one is left in the room, remove the room entry from the dictionary
        if not rooms[self.room_group_name]:
            del rooms[self.room_group_name]

        # Notify the remaining members in the room of the updated count
        if self.room_group_name in rooms:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'people_in_chat_quantity',
                    'data': {
                        'type': 'people_in_chat_quantity',
                        'count': len(rooms[self.room_group_name]) - 1,
                    }
                }
            )

    async def receive(self, text_data):
        data = json.loads(text_data)

        message_body = data['message']
        from_user_id = data['from_user_id']
        to_user_id = data['to_user_id']

        # Save the message to the database
        saved_message = await self.save_message(from_user_id, to_user_id, message_body)

        # Send the saved message back to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_message',
                'data': {
                    'type': 'message',
                    'from_user_id': from_user_id,
                    'to_user_id': to_user_id,
                    'message': saved_message.body,  # Use the body of the saved message
                    'date': (saved_message.created + timedelta(hours=5)).isoformat()  # Format date nicely
                }
            }
        )

    async def send_message(self, event):
        await self.send(text_data=json.dumps(event['data']))

    async def people_in_chat_quantity(self, event):
        await self.send(text_data=json.dumps(event['data']))

    async def send_message_history(self, message_history):
        # Send the message history to the connected client
        await self.send(text_data=json.dumps({
            'type': 'message_history',
            'data': message_history
        }))

    @database_sync_to_async
    def save_message(self, from_user_id, to_user_id, message_body) -> Message:
        from_user = User.objects.get(id=from_user_id)
        to_user = User.objects.get(id=to_user_id)
        message = Message.objects.create(
            from_user=from_user,
            to_user=to_user,
            body=message_body
        )
        return message

    @database_sync_to_async
    def get_message_history(self):
        # Retrieve all messages for the current chat room

        messages = Message.objects.filter(
            Q(Q(from_user__username=self.user.username) & Q(to_user__username=self.room_name)) |
            Q(Q(from_user__username=self.room_name) & Q(to_user__username=self.user.username))
        )

        return [
            {
                'from_user_id': message.from_user.id,
                'to_user_id': message.to_user.id,
                'message': message.body,
                'date': (message.created + timedelta(hours=5)).isoformat()
            } for message in messages.order_by('created')
        ]


    