from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    username = models.CharField(max_length=30)

    def __str__(self):
        return "%s" % (self.username)


class WebSocket(models.Model):
    room_name = models.CharField(max_length=32)
    token = models.CharField(max_length=32)
    timestamp = models.DateTimeField(auto_now_add=True)
    username_websocket = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.room_name
