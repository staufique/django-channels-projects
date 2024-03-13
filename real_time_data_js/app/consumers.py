from channels.consumer import SyncConsumer
from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
from time import sleep
import json
import asyncio
class MySyncConsumer(SyncConsumer):

    def websocket_connect(self,event):
        print("websocket Connected...",event)
        self.send({"type":"websocket.accept"})

    def websocket_receive(self,event):
        print("Message Received...",event)
        print("Message Received...",event['text'])
        for i in range(1,11):
            self.send({"type":"websocket.send","text":json.dumps({'count':i})})
            sleep(1)

    def websocket_disconnect(self,event):
        print("Websocket Disconnected...",event)
        raise StopConsumer()
 
class MyASyncConsumer(AsyncConsumer):

    async def websocket_connect(self,event):
        print("websocket Connected...",event)
        await self.send({"type":"websocket.accept"})

    async def websocket_receive(self,event):
        print("Message Received...",event)
        print("Message Received...",event['text'])
        for i in range(1,11):
            await self.send({"type":"websocket.send","text":str(i)})
            await asyncio.sleep(1)

    async def websocket_disconnect(self,event):
        print("Websocket Disconnected...",event)
        raise StopConsumer()