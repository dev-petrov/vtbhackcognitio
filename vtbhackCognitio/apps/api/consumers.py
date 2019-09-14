from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
from index.models import Comment
from channels.db import database_sync_to_async
import time


class MessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Called on connection.
        # To accept the connection call:
        await self.accept()
        # Or accept the connection and specify a chosen subprotocol.
        # A list of subprotocols specified by the connecting client
        # will be available in self.scope['subprotocols']
        #await self.accept("subprotocol")
        # To reject the connection, call:
        #await self.close()

    async def receive(self, text_data=None, bytes_data=None):
        # Called with either text_data or bytes_data for each frame
        # You can call:
        async def get_new_comments(self, date):
            self.comments = await search_for_new_comments(self, date)
        @database_sync_to_async
        def search_for_new_comments(self, date):
            return Comment.objects.filter(date__gt=date)
        await asyncio.sleep(1)
        comments = await get_new_comments(self, date = '2000-09-25 8:30:34')
        print(comments)
        await self.send(text_data=text_data)
        # Or, to send a binary frame:
        #await self.send(bytes_data="Hello world!")
        # Want to force-close the connection? Call:
        #await self.close()
        # Or add a custom WebSocket error code!
        #await self.close(code=4123)

    async def disconnect(self, close_code):
        # Called when the socket closes
        pass
