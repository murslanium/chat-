from django.contrib.auth.models import User
from django.db import models


class Room(models.Model):
    name = models.TextField()


class Message(models.Model):
    message = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(to=User, on_delete=models.RESTRICT)
    room = models.ForeignKey(to=Room, on_delete=models.RESTRICT)


class UserRooms(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.RESTRICT)
    room = models.ForeignKey(to=Room, on_delete=models.RESTRICT)
