import json
from channels.generic.websocket import AsyncWebsocketConsumer
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # User authentication check
        if self.scope['user'].is_anonymous:
            # If user is not authenticated, close the connection
            await self.close()
        else:
            # Join chat room
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        # Leave chat room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message or typing data from WebSocket
    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json.get('message')
            typing = text_data_json.get('typing')
            user = self.scope['user']  # Get authenticated user

            # Handle typing event if present
            if typing is not None:
                # Broadcast typing event to others in the room, excluding the sender
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'user_typing',
                        'typing': typing,
                        'sender_channel_name': self.channel_name  # Send sender's channel name
                    }
                )

            # Handle message if present
            if message:
                # Broadcast message to room group with user info
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'user': user.username  # Include user's name
                    }
                )

        except json.JSONDecodeError:
            print("Invalid JSON received")

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        user = event['user']  # Get user name from the event

        # Send message to WebSocket with user info
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user  # Include user's name in the response
        }))

    # Handle typing event broadcast
    async def user_typing(self, event):
        typing = event['typing']
        sender_channel_name = event['sender_channel_name']

        # Only send typing notification to other users (not the sender)
        if self.channel_name != sender_channel_name:
            await self.send(text_data=json.dumps({
                'typing': typing,
            }))
