from django.urls import path,include
from . import views

app_name='group'

urlpatterns = [
        path('signup',views.signup, name= 'signup'),
        path('',views.login, name= 'login'),        
        path('logout',views.logout, name= 'logout'),        
        path('chatlist/<str:username>/<str:password>',views.chatlist, name= 'chatlist'),        
        path('chat/<str:username>/<str:password>/<int:groupid>',views.chat, name= 'chat'),        
        path('securechat/<str:username>/<str:password>/<int:groupid>',views.securechat, name= 'securechat'),        
        path('replymessage/<str:username>/<str:password>/<int:groupid>/<int:msgid>',views.replymessage, name= 'replymessage'),        
        path('media/<str:file>',views.load_file, name= 'load_file'),        
        path('media/<str:secure>/<str:file>',views.load_file_secure, name= 'load_file_secure'),
]