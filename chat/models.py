from django.contrib.auth import get_user_model
from post.models import *
from django.db import models


class ChatRoom(models.Model):
    objects = models.Manager


class ChatRoomUser(models.Model):
    chat_room = models.ForeignKey(ChatRoom,on_delete=False,
                                  related_name="roomuser_roomid")
    user = models.ForeignKey(User,on_delete=False,related_name="roomuser_userid")
    objects = models.Manager


class ChatMessage(models.Model):
    chat_room = models.ForeignKey(ChatRoom,on_delete=False,
                                  related_name="message_roomid")
    user = models.ForeignKey(User,on_delete=False,related_name="message_userid")
    message = models.CharField(max_length=500)
    objects = models.Manager







