from django.contrib import admin

from chat import models

class ConfigUser(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'username')

class ConfigWebSocket(admin.ModelAdmin):
    list_display = ('id', 'room_name', 'user_websocket' ,'timestamp')

admin.site.register(models.User, ConfigUser)
admin.site.register(models.WebSocket, ConfigWebSocket)