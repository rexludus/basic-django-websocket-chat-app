from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html', {})

def no_room(request):
    return render(request, 'chatroom.html', {})