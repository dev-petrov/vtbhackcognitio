from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
import asyncio
from index.models import Comment, Result
from channels.db import database_sync_to_async
import datetime, json
from index.serializers import CommentSerializer, ResultSerializer


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
        print(text_data)
        data = json.loads(text_data)

        async def get_new_comments(self):
            self.comments = await database_sync_to_async(search_for_new_comments)(self)
        def search_for_new_comments(self):
            return Comment.objects.filter(doc_id = int(data['doc_id']), date__lt=data['date']).exclude(user = data['user'])
        
        for i in range(5):
            comments = Comment.objects.filter(doc_id = int(data['doc_id']), date__gt=data['date']).exclude(user = data['user'])#await get_new_comments(self, date = data[0])
            await asyncio.sleep(2)

            if (comments.count() != 0):
                break

        if (comments.count() != 0):
            data = {
                'type': 'found',
                'comments':CommentSerializer(comments, many = True).data
            }
            text_data = str(json.dumps(data, ensure_ascii=False))
            print(text_data)
        else:
            text_data = json.dumps({
                'type': 'nothing new'
            })
        print('Sented')
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

class ResultConsumer(AsyncWebsocketConsumer):
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
        data = json.loads(text_data)
        async def get_new_comments(self, date):
            self.comments = await search_for_new_comments(self, date)
        @database_sync_to_async
        def search_for_new_comments(self, date):
            return Comment.objects.filter(date__gt=date)
        for i in range(10):
            results = Result.objects.filter(doc_id = int(data['doc_id']), date__gt=data['date']).exclude(user = data['user'])
            await asyncio.sleep(1)
            if (results.count() != 0):
                break
        #comments = await get_new_comments(self, date = '2000-09-25 8:30:34')
        #print(comments)
        if (comments.count() != 0):
            data = {
                'type': 'found',
                'results':ResultSerializer(results, many = True).data
            }
            text_data = str(json.dumps(data, ensure_ascii=False))
            print(text_data)
        else:
            text_data = json.dumps({
                'type': 'nothing new'
            })
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

"""class MessageConsumer(AsyncJsonWebsocketConsumer):
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

    async def receive_json(self, content = None):
        # Called with either text_data or bytes_data for each frame
        # You can call:
        date = content['date']
        doc = content['doc_id']

        
        for i in range(10):
            comments = Comment.objects.filter(doc_id = int(doc), date__gt=date)#await get_new_comments(self, date = data[0])
            if (comments.count() != 0):
                break
            await asyncio.sleep(1)

        if (comments.count() != 0):
            data = {
                'type': 'found',
                'comments':CommentSerializer(comments, many = True).data
            }
        else:
            data = {
                'type': 'nothing new'
            }
        print('Sented')
        await self.send_json(content=data)
        # Or, to send a binary frame:
        #await self.send(bytes_data="Hello world!")
        # Want to force-close the connection? Call:
        #await self.close()
        # Or add a custom WebSocket error code!
        #await self.close(code=4123)

    async def disconnect(self, close_code):
        # Called when the socket closes
        pass"""