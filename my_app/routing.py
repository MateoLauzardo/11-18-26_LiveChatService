# NOTE routing.py is the real-time equivalent of urls.py—it
# maps incoming WebSocket (or other ASGI protocol) paths to 
# the specific consumers in consumers.py that handle them.


from django.urls import re_path
from . import consumers

from channels.generic.websocket import AsyncWebsocketConsumer
import json
import uuid


websocket_urlpatterns = [
    re_path(r'ws/chat/$', consumers.ChatConsumer.as_asgi())
] 


waiting_users = []


# creates a new ChatConsumer object for each WebSocket connection.
class ChatConsumer(AsyncWebsocketConsumer):
    
       
    
    # when someone opens wep socket this method runs automatically. 
    async def connect(self):
        
        
        
        # represents the users connection)
        user_connection = self.channel_name
            
                
        # if someone is waiting -> connect user to first room 
        if waiting_users:
            
            # grab index 0 (first room)
            first_room_we_grabbed = waiting_users[0]
            
            # pop room from array 
            del waiting_users[0]
            
            
            # Get the existing room (Shared room)
            self.room_group_name = first_room_we_grabbed["room_group_name"]
            
            
            # adds channel
            await self.channel_layer.group_add(
                self.room_group_name, 
                user_connection # the current user
            )
            
            await self.accept()
        
        
        
        # nobody is waiting -> create room, adds user to room          
        else:
            
            # create new room from a random room name script 
            room_name = str(uuid.uuid4())[:8]


            # create room 
            self.room_group_name = f"chat_{room_name}"
            
                
            # add to waiting users_array (hashmap)
            waiting_users.append({
                "user_connection": user_connection,
                "room_group_name": self.room_group_name
            })
            
            
            # adds channel
            await self.channel_layer.group_add(
                self.room_group_name, # Which group
                user_connection # Which connection/user
            )
            
            await self.accept()
