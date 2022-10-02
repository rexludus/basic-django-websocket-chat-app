from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html', {})

def no_room(request):
    return render(request, 'chatroom.html', {})

def room(request, room_name_mobile):
    return render(request, 'chatroom.html', {
        'room_name_mobile': room_name_mobile
    })