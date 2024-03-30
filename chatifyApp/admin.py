# username = chatify
# pass = chatify
# email = chatify@gmail.com

from django.contrib import admin

from .models import User
from .models import Themes, Friend_List, Groups, Group_Members, Chats, Group_chat

# # Register your models here.

admin.site.register(User)
admin.site.register(Themes)
admin.site.register(Friend_List)
admin.site.register(Groups)
admin.site.register(Group_Members)
admin.site.register(Chats)
admin.site.register(Group_chat)


