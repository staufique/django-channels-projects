from channels.consumer import SyncConsumer
from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
class MySyncConsumer(SyncConsumer):

    def websocket_connect(self,event):
        print("websocket Connected...",event)
        self.send({"type":"websocket.accept"})

    def websocket_receive(self,event):
        print("Message Received...",event)
        print("Message Received...",event['text'])

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

    async def websocket_disconnect(self,event):
        print("Websocket Disconnected...",event)
        raise StopConsumer()