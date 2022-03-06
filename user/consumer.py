import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import User

   

class NotifyConsumer(WebsocketConsumer):
    def connect(self):
        channel = self.scope['url_route']['kwargs']['room_name']
        user=User.objects.get(channel=channel)
        #self.room_name = user.room
        self.room_group_name =user.group

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        name = text_data_json['name']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'name': name
            }
        )

    # Receive message from room group
    def notify(self,event):
        print(event)
        self.send(json.dumps(event.get('value')))
        
    