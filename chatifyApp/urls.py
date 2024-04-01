from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('index',views.index,name='index'),
    path('home',views.home,name='home'),
    path('signup',views.signup,name='signup'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('setting',views.setting,name='setting'),
    path('notification',views.notification,name='notification'),
    path('store',views.store,name='store'),
    path('chatWithFriend/<str:friend_id>/',views.chatWithFriend,name='chatWithFriend'),
    path('sendMsg',views.sendMsg,name='sendMsg'),
]