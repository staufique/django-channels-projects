from channels.consumer import SyncConsumer,AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync

class MySyncConsumer(SyncConsumer):
    def websocket_connect(self,event):
        print("websocket connected...",event)
        print("channel Layer...",self.channel_layer)
        print("channel Name...",self.channel_name)

        self.group_name=self.scope['url_route']['kwargs']['groupName']

        async_to_sync(self.channel_layer.group_add)(self.group_name,self.channel_name)

        self.send({"type":"websocket.accept","text":"hello"})

    def websocket_receive(self,event):
        print("message received from client...",event)
        async_to_sync(self.channel_layer.group_send)(
             self.group_name,{
            'type':'chat.message',
            'message':event['text']}
        )

    def chat_message(self,event):
        print('Event...',event['message'])
        self.send({
            'type':'websocket.send',
            'text':event['message']
        })

    def websocket_disconnect(self,event):
        print("websocket disconnected...",event)
        print("channel Layer...",self.channel_layer)
        print("channel Name...",self.channel_name)
        async_to_sync(self.channel_layer.group_discard)(self.group_name,self.channel_name)
        raise StopConsumer()

class MyASyncConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        print("websocket connected...",event)
        print("channel Layer...",self.channel_layer)
        print("channel Name...",self.channel_name)
        self.group_name=self.scope['url_route']['kwargs']['groupName']

        await self.channel_layer.group_add(self.group_name,self.channel_name)

        await self.send({"type":"websocket.accept","text":"hello"})

    async def websocket_receive(self,event):
        print("message received from client...",event)
        await self.channel_layer.group_send(
            self.group_name,{
            'type':'chat.message',
            'message':event['text']}
        )

    async def chat_message(self,event):
        print('Event...',event['message'])
        await self.send({
            'type':'websocket.send',
            'text':event['message']
        })

    async def websocket_disconnect(self,event):
        print("websocket disconnected...",event)
        print("channel Layer...",self.channel_layer)
        print("channel Name...",self.channel_name)
        await self.channel_layer.group_discard(self.group_name,self.channel_name)
        raise StopConsumer()