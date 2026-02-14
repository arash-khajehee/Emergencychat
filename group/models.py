from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.conf import settings

# Create your models here.

class AllUser(models.Model):
    alluser_username = models.CharField(unique=True, max_length=100)
    alluser_password = models.CharField(max_length=100)
    def __str__(self):
        return self.alluser_username + " : " + self.alluser_password

class Group(models.Model):
    group_title = models.CharField(unique=True, max_length=100)
    group_member = models.ManyToManyField("AllUser",blank=True)
    group_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.group_title
    
    
class Messages(models.Model):
    messages_group = models.ForeignKey("Group", on_delete=models.CASCADE)    
    messages_member = models.ForeignKey("AllUser", on_delete=models.CASCADE)
    messages_text = models.TextField()
    messages_file = models.FileField(blank=True)
    messages_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.messages_text) + "   :   " + str(self.messages_group.group_title)
    
    


class SecureGroup(models.Model):
    securegroup_title = models.CharField(unique=True, max_length=100)
    securegroup_member = models.ManyToManyField("AllUser",blank=True)
    securegroup_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.securegroup_title


class SecureMessages(models.Model):
    securemessages_group = models.ForeignKey("SecureGroup", on_delete=models.CASCADE)    
    securemessages_member = models.ForeignKey("AllUser", on_delete=models.CASCADE)
    securemessages_replymessage = models.ForeignKey("SecureMessages", on_delete=models.CASCADE, null=True)
    securemessages_text = models.TextField(blank=True)
    securemessages_file = models.FileField(upload_to="secure/",blank=True)
    securemessages_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.securemessages_group.securegroup_title) + " : " + str(self.securemessages_time) 
    
    
    