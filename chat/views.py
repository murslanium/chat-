from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .models import UserRooms, Room, Message


@login_required
def home(request):
    return redirect(chat)


def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    else:
        first_name = request.POST["first_name"]
        email = request.POST["email"]
        password = request.POST["password"]
        user = User(username=email, password=password, email=email, first_name=first_name)
        validationResult = __validate_user(user)
        if len(validationResult) != 0:
            return render(request, "register.html", {"user": user, "validationResult": validationResult})
        else:
            user = User.objects.create_user(user.username, user.email, user.password, first_name=user.first_name)
            return render(request, "auth.html", {"userData": user})


def auth(request):
    if request.method == "GET":
        return render(request, "auth.html", {})
    else:
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)
        if user is None:
            return render(request, "auth.html", {"authError": True, "email": email})

        login(request, user)
        return redirect(chat)


@login_required
def chat(request, room_id=None):
    user_rooms = UserRooms.objects.filter(user=request.user)
    available_rooms = map(lambda x: x.room, user_rooms)
    if len(user_rooms) > 0 and room_id is None:
        room_id = user_rooms[0].room.id

    room_users = UserRooms.objects.filter(room_id=room_id)
    users = map(lambda x: x.user, room_users)
    messages = Message.objects.filter(room=room_id).order_by('time')
    return render(request, "chat.html", {
        "current_room": room_id,
        "available_rooms": available_rooms,
        "messages": messages,
        "users": users
    })


@login_required
def create_room(request):
    if request.method == "GET":
        return render(request, "create_room.html", {"hasError": False})
    room_name = request.POST["roomName"]
    if not room_name:
        return render(request, "create_room.html", {"hasError": False})
    room = Room(name=room_name)
    room.save()
    UserRooms(user=request.user, room=room).save()
    return redirect(chat)


def logout_user(request):
    logout(request)
    return redirect(auth)


def __validate_user(user):
    result = {}
    if not user.first_name:
        result["first_name"] = "ФИО не указаны"
    if not user.password:
        result["password"] = "Пароль не указан"
    if not user.email:
        result["email"] = "Email не указан"
    else:
        users = User.objects.filter(username=user.email)
        if len(users) != 0:
            result['email'] = "Пользователь с данным ящиком уже зарегистрирован"
    return result


@login_required
def send(request):
    msg = request.POST["message"]
    roomId = request.POST["room"]
    if not msg or not roomId:
        raise ValueError()
    Message.objects.create(message=msg, room_id=roomId, sender=request.user)
    messages = Message.objects.filter(room=roomId).order_by('time')
    return render(request, "message_list.html", {"messages": messages})


@login_required
def message_list(request, room_id):
    messages = Message.objects.filter(room=room_id).order_by('time')
    return render(request, "message_list.html", {"messages": messages})


@login_required
def attach_user(request, room_id):
    userId = request.POST["userId"]
    if len(UserRooms.objects.filter(user_id=userId, room_id=room_id)) != 0:
        return get_user_list(request, room_id)
    if len(User.objects.filter(id=userId))==0:
        raise ValueError("Пользователь не найден")
    UserRooms.objects.create(user_id=userId, room_id=room_id)
    return get_user_list(request, room_id)


def get_user_list(request, room_id):
    room_users = UserRooms.objects.filter(room_id=room_id)
    users = map(lambda x: x.user, room_users)
    return render(request, "user_list.html", {"users": users})
