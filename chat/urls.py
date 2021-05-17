from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register', views.register, name="register"),
    path('auth', views.auth, name="auth"),
    path('chat', views.chat, name="chat"),
    path('chat/<int:room_id>', views.chat, name="chat"),
    path('logout', views.logout_user, name="logout"),
    path('createroom', views.create_room, name="create_room"),
    path('send', views.send, name="send_message"),
    path('message_list/<int:room_id>', views.message_list, name="message_list"),
    path('attach_user/<int:room_id>', views.attach_user, name="attach_user")
]
