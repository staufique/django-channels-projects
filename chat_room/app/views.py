from django.shortcuts import render
from .models import Group,Chat

def index(request,group_name="programmers"):

    group = Group.objects.filter(name=group_name).first()

    chats=[]
    if group:
        chats=Chat.objects.filter(group=group)
    else:
        group=Group(name=group_name)
        group.save()
    return render(request,'index.html',{'groupname':group_name,'chats':chats})