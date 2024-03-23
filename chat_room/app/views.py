from django.shortcuts import render

# Create your views here.

def index(request,group_name="programmers"):
    return render(request,'index.html',{'groupname':group_name})