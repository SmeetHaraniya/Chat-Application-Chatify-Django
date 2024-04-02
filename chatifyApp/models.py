from django.db import models
# # Create your models here.

from django.contrib.auth.models import AbstractUser,User,auth
# from .models import UserInfo

class Themes(models.Model):
    theme_id = models.BigAutoField(primary_key=True,null=False,blank=False)
    theme_name = models.CharField(max_length=255, null=False)
#     # theme_photo = 
    price = models.IntegerField()

class User(AbstractUser):
    user_id = models.CharField(max_length=50,primary_key=True,null=False,blank=False)
    dob = models.DateField(null=True)
    phoneno = models.IntegerField(null=True)
    coins = models.IntegerField(default=100)
    theme_id = models.ForeignKey(Themes,on_delete=models.CASCADE,to_field='theme_id',default=1)

class Friend_List(models.Model):
    class Meta:
        unique_together = (('user_id', 'friend_id'),)
    user_id = models.ForeignKey(User,to_field='user_id',on_delete=models.CASCADE,related_name='friend_list_user_id')
    friend_id = models.ForeignKey(User,to_field='user_id',on_delete=models.CASCADE,related_name='friend_list_friend_id')
    friend_since = models.DateField(null=True)
    friend_status = models.CharField(max_length=10,default='pending')
    last_chat_date = models.DateField(null=True)
    last_chat_time = models.TimeField(null=True)

class Chats(models.Model):
    sender_id = models.ForeignKey(User,to_field='user_id',on_delete=models.CASCADE,related_name='chat_sender_id')
    receiver_id = models.ForeignKey(User,to_field='user_id',on_delete=models.CASCADE,related_name='chat_receiver_id')
    msg = models.TextField()
    msg_time = models.TimeField(null=True)
    msg_date = models.DateField(null=True)


class Groups(models.Model):
    group_id = models.BigAutoField(primary_key=True,null=False,blank=False)
    group_name = models.CharField(max_length=255,null=False)
    group_admin = models.ForeignKey(User,to_field='user_id',on_delete=models.CASCADE,related_name='groups_admin') #cascade....
    create_date = models.DateField(null=True)

class Group_Members(models.Model):
    class Meta:
        unique_together = (('user_id', 'group_id'),)
    user_id = models.ForeignKey(User,to_field='user_id',on_delete=models.CASCADE,related_name='group_member_user_id')
    group_id = models.ForeignKey(Groups,to_field='group_id',on_delete=models.CASCADE,related_name='group_member_group_id')

class Group_chat(models.Model):
    group_id = models.ForeignKey(Groups,to_field='group_id',on_delete=models.CASCADE,related_name='group_chat_id')
    sender_id = models.ForeignKey(User,to_field='user_id',on_delete=models.CASCADE,related_name='group_chat_sender_id')
    msg = models.TextField()   
    

