from django.shortcuts import render , redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse,FileResponse
from .models import *
import os
import time
import json
from django.http import StreamingHttpResponse
from django.template.loader import render_to_string
# Create your views here.


def logout(request):
    response = redirect('group:login')
    response.set_cookie(
        key='username',
        value="",
        max_age=3600000,
    )
    response.set_cookie(
        key='password',
        value="",
        max_age=3600000,
    )
    return response


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user_obj = AllUser.objects.create(
                alluser_username = username ,
                alluser_password = password
            )
            user_obj.save()

            group, created = Group.objects.get_or_create(group_title="main_group")
            group.group_member.add(user_obj)
        
        
            return redirect('group:login')
        except:
            return render(request,'signup.html')

    
    return render(request,'signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        obj = AllUser.objects.filter(alluser_username = username, alluser_password = password).exists()
        if obj:
            response = redirect('group:chatlist',username = username,password = password)
            response.set_cookie(
                key='username',
                value=username,
                max_age=3600000,
            )
            response.set_cookie(
                key='password',
                value=password,
                max_age=3600000,
            )
            return response
        else:
            return render(request,'login.html')
    
    try:
        username = request.COOKIES.get('username')
        password = request.COOKIES.get('password')
        obj_user = AllUser.objects.filter(alluser_username = username, alluser_password = password).exists()
        if obj_user : 
            return redirect('group:chatlist',username = username,password = password)
        
    except:    
        return render(request,'login.html')
    
    return render(request,'login.html')


def chatlist(request,username,password):
    obj = AllUser.objects.get(alluser_username = username, alluser_password = password)
    all_group = Group.objects.filter(group_member = obj)
    all_secure_group = SecureGroup.objects.filter(securegroup_member = obj)
    context = {
        "all_group" : all_group ,
        "all_secure_group" : all_secure_group ,
        "username" : username ,
        "password" : password
    }
    return render(request,'chatlist.html',context)


def chat(request,username,password,groupid):
    if request.method == 'POST':
        
        text = request.POST['text']
        try:
            file = request.FILES['file']
        except:
            file = ""  
            
        user_obj = AllUser.objects.get(alluser_username = username, alluser_password = password)
        obj_group = Group.objects.get(id = groupid)    
        msg_obj = Messages.objects.create(
            messages_group = obj_group,
            messages_member = user_obj,
            messages_text = text,
            messages_file = file,
        )
        msg_obj.save()
        
        return redirect('group:chat',username=username, password=password, groupid=groupid)
    
    user_obj = AllUser.objects.get(alluser_username = username, alluser_password = password)
    obj_group = Group.objects.get(id = groupid)
    all_message = Messages.objects.filter(messages_group = obj_group).order_by('-messages_time')
    paginator = Paginator(all_message, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if Group.objects.filter(id = groupid,group_member=user_obj).exists():
        user_obj = AllUser.objects.get(alluser_username = username, alluser_password = password)
        obj_group = Group.objects.get(id = groupid)
        all_message = Messages.objects.filter(messages_group = obj_group).order_by('-messages_time')
        member_no = obj_group.group_member.count()
        context = {
            "all_message" : all_message ,
            "page_obj" : page_obj ,
            "user_obj" : user_obj ,
            "username" : username ,
            "password" : password ,
            "obj_group" : obj_group ,
            "member_no" : member_no
        }
        return render(request,'chat.html',context)
    
    else :
        return redirect('group:chatlist',username=username, password=password)
    




def securechat(request,username,password,groupid):
    if request.method == 'POST':
        
        text = request.POST['text']
        try:
            file = request.FILES['file']
        except:
            file = ""  
            
        user_obj = AllUser.objects.get(alluser_username = username, alluser_password = password)
        obj_group = SecureGroup.objects.get(id = groupid)    
        msg_obj = SecureMessages.objects.create(
            securemessages_group = obj_group,
            securemessages_member = user_obj,
            securemessages_text = text,
            securemessages_file = file,
        )
        msg_obj.save()
        
        return redirect('group:securechat',username=username, password=password, groupid=groupid)
    
    user_obj = AllUser.objects.get(alluser_username = username, alluser_password = password)
    obj_group = SecureGroup.objects.get(id = groupid)
    all_message = SecureMessages.objects.filter(securemessages_group = obj_group).order_by('-securemessages_time')
    paginator = Paginator(all_message, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if SecureGroup.objects.filter(id = groupid,securegroup_member=user_obj).exists():
        user_obj = AllUser.objects.get(alluser_username = username, alluser_password = password)
        obj_group = SecureGroup.objects.get(id = groupid)
        all_message = SecureMessages.objects.filter(securemessages_group = obj_group).order_by('-securemessages_time')
        member_no = obj_group.securegroup_member.count()
        context = {
            "all_message" : all_message ,
            "page_obj" : page_obj ,
            "user_obj" : user_obj ,
            "username" : username ,
            "password" : password ,
            "obj_group" : obj_group ,
            "member_no" : member_no
        }
        return render(request,'securechat.html',context)
    
    else :
        return redirect('group:chatlist',username=username, password=password)



def replymessage(request,username,password,groupid,msgid):
    if request.method == 'POST':
        
        text = request.POST['text']
        try:
            file = request.FILES['file']
        except:
            file = ""  
            
        user_obj = AllUser.objects.get(alluser_username = username, alluser_password = password)
        obj_group = SecureGroup.objects.get(id = groupid)    
        source_msg = SecureMessages.objects.get(id=msgid)
        msg_obj = SecureMessages.objects.create(
            securemessages_group = obj_group,
            securemessages_member = user_obj,
            securemessages_replymessage = source_msg,
            securemessages_text = text,
            securemessages_file = file,
        )
        msg_obj.save()
        
        return redirect('group:securechat',username=username, password=password, groupid=groupid)
    
    user_obj = AllUser.objects.get(alluser_username = username, alluser_password = password)
    obj_group = SecureGroup.objects.get(id = groupid)
    all_message = SecureMessages.objects.filter(id = msgid).order_by('-securemessages_time')
    paginator = Paginator(all_message, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if SecureGroup.objects.filter(id = groupid,securegroup_member=user_obj).exists():
        user_obj = AllUser.objects.get(alluser_username = username, alluser_password = password)
        obj_group = SecureGroup.objects.get(id = groupid)
        all_message = SecureMessages.objects.filter(id = msgid).order_by('-securemessages_time')
        member_no = obj_group.securegroup_member.count()
        context = {
            "all_message" : all_message ,
            "page_obj" : page_obj ,
            "user_obj" : user_obj ,
            "username" : username ,
            "password" : password ,
            "obj_group" : obj_group ,
            "member_no" : member_no
        }
        return render(request,'replymessage.html',context)
    
    else :
        return redirect('group:chatlist',username=username, password=password)


    
def load_file (request,file) :
    document = get_object_or_404(Messages,messages_file = file)
    path,file_name = os.path.split(file)
    response = FileResponse(document.messages_file)
    return response     


def load_file_secure (request,secure,file) :
    if secure == "secure" :
        document = get_object_or_404(SecureMessages,securemessages_file = "secure/"+file)
    path,file_name = os.path.split(file)
    response = FileResponse(document.securemessages_file)
    return response  