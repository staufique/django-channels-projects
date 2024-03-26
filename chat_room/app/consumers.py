import json
from channels.consumer import SyncConsumer,AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
from .models import Group,Chat
from channels.db import database_sync_to_async

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
        data=json.loads(event['text'])

        group = Group.objects.get(name=self.group_name)
        data['user'] = self.scope['user'].username
        print(data['user'])
        if self.scope['user'].is_authenticated:
            chat = Chat(content=data['msg'],group=group)
            chat.save()
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,{
                'type':'chat.message',
                'message':json.dumps(data)}
            )
        else:
           self.send({
                'type':'websocket.send',
                'text':json.dumps({"msg":"Login required",'user':'guest'})
                })

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
    # def websocket_connect(self,event):
    #     print("websocket connected...",event)
    #     print("channel Layer...",self.channel_layer)
    #     print("channel Name...",self.channel_name)

    #     self.group_name=self.scope['url_route']['kwargs']['groupName']

    #     async_to_sync(self.channel_layer.group_add)(self.group_name,self.channel_name)

    #     self.send({"type":"websocket.accept","text":"hello"})

    # def websocket_receive(self,event):
    #     print("message received from client...",event)
    #     data=json.loads(event['text'])
    #     print(data)
    #     group = Group.objects.get(name=self.group_name)
    #     print(self.scope['user'])
    #     if self.scope['user'].is_authenticated:
    #         chat = Chat(content=data['msg'],group=group)
    #         chat.save()
    #         async_to_sync(self.channel_layer.group_send)(
    #             self.group_name,{
    #             'type':'chat.message',
    #             'message':event['text']}
    #         )
    #     else:
    #        self.send({
    #             'type':'websocket.send',
    #             'text':json.dumps({"msg":"Login required"})
    #             })

    # def chat_message(self,event):
    #     print('Event...',event['message'])
    #     self.send({
    #         'type':'websocket.send',
    #         'text':event['message']
    #     })

    # def websocket_disconnect(self,event):
    #     print("websocket disconnected...",event)
    #     print("channel Layer...",self.channel_layer)
    #     print("channel Name...",self.channel_name)
    #     async_to_sync(self.channel_layer.group_discard)(self.group_name,self.channel_name)
    #     raise StopConsumer()

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

        data=json.loads(event['text'])
        print(data)
        group = await database_sync_to_async(Group.objects.get)(name=self.group_name)
        data['user'] = self.scope['user'].username
        if self.scope['user'].is_authenticated:
            chat = Chat(content=data['msg'],group=group)
            await database_sync_to_async(chat.save)()

            await self.channel_layer.group_send(
                self.group_name,{
                'type':'chat.message',
                'message':json.dumps(data)}
            )
        else:
            await self.send({
                'type':'websocket.send',
                'text':json.dumps({"msg":"Login required",'user':'guest'})
                })

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
# class MyASyncConsumer(AsyncConsumer):
#     async def websocket_connect(self,event):
#         print("websocket connected...",event)
#         print("channel Layer...",self.channel_layer)
#         print("channel Name...",self.channel_name)
#         self.group_name=self.scope['url_route']['kwargs']['groupName']

#         await self.channel_layer.group_add(self.group_name,self.channel_name)

#         await self.send({"type":"websocket.accept","text":"hello"})

#     async def websocket_receive(self,event):
#         print("message received from client...",event)

#         data=json.loads(event['text'])
#         print(data)
#         group = await database_sync_to_async(Group.objects.get)(name=self.group_name)
        
#         if self.scope['user'].is_authenticated:
#             chat = Chat(content=data['msg'],group=group)
#             await database_sync_to_async(chat.save)()

#             await self.channel_layer.group_send(
#                 self.group_name,{
#                 'type':'chat.message',
#                 'message':event['text']}
#             )
#         else:
#             await self.send({
#                 'type':'websocket.send',
#                 'text':json.dumps({"msg":"Login required"})
#                 })

#     async def chat_message(self,event):
#         print('Event...',event['message'])
#         await self.send({
#             'type':'websocket.send',
#             'text':event['message']
#         })

#     async def websocket_disconnect(self,event):
#         print("websocket disconnected...",event)
#         print("channel Layer...",self.channel_layer)
#         print("channel Name...",self.channel_name)
#         await self.channel_layer.group_discard(self.group_name,self.channel_name)
#         raise StopConsumer()