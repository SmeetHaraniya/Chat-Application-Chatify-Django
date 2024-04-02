from django.shortcuts import render,redirect
from django.http import HttpResponse

from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import User,Themes, Friend_List, Groups, Group_Members, Chats, Group_chat

from django.utils import timezone
from datetime import datetime,date,timedelta
from django.db.models import Q


# Create your views here.

def home(request):
    if request.method == 'POST':
        return render(request,'index.html');
    else:
        return render(request,'login.html');

def login(request):
    request.session.flush()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            print('login successfully')
            request.session['username'] = username
            return redirect('index')
        else:
            messages.error(request,'Invalid credential !!')
            return render(request,'login.html')
    else:
        print('not posted in login')    
        return render(request,'login.html')

def signup(request):
    if request.method == 'POST':
        firstname = request.POST['firstName']
        lastname = request.POST['lastName']
        dob = request.POST['dob']
        phoneno = request.POST['phoneNo']
        username = request.POST['userName']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if password==cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username already exists !!")
                print("username exist")
                return redirect('signup')
            elif User.objects.filter(phoneno=phoneno).exists():
                messages.error(request,"MobileNo already exists !!")
                print("mobile exist")
                return redirect('signup')
            else:
                # themeobj = Themes.objects.all()
                #  user = User.objects.create_user(username=username,password=password,first_name=fname,last_name=lname)
                user = User.objects.create_user(first_name=firstname,last_name=lastname,user_id=username,username=username,dob=dob,phoneno=phoneno,password=password)
                user.save()
                print("signup successfully")
                return redirect('login')
        else:
            messages.info(request,'Password does not match !!')
            print("passwrod not match")
            return redirect('signup')
    else:
        return render(request,'signup.html')

def setting(request):
    if request.session.get('username') is None:
        return redirect('login')

    if request.method == 'POST':
        username = request.POST['username']
        mobileno = request.POST['mobileno']
        password = request.POST['Password']
        cpassword = request.POST['cPassword']
        print(username)
        print(mobileno)
        print(password)
        print(cpassword)

        if password==cpassword:
            username = request.session.get('username')
            userlist = User.objects.filter (username=username,phoneno=mobileno)
            user = userlist.first()
            print(username)
            if user:
                user.set_password(password)
                user.save()
                messages.info(request,"Password was changed successfully !!")
            else:
                messages.error(request,"Invalid Credentials !!")
        else:
            messages.error(request,"Password does not match !!")
    
    return render(request,'setting.html')

def notification(request):
    if request.session.get('username') is None:
        return redirect('login')

    username = request.session.get('username')
    if request.method == 'POST':
        if 'frnd' in request.POST:
            frnd = request.POST.get('frnd')
            print(frnd)
            try :
                frndObj = Friend_List.objects.filter(user_id=username,friend_id=frnd) | Friend_List.objects.filter(user_id=frnd,friend_id=username)
                obj = frndObj.first()
                # print("obj")
                obj.friend_status = "accept"
                obj.save()
            except Exception as e:
                print(e)
        else: 
            frnd = request.POST.get('reject')
            print(username)
            print(frnd)
            frndObj = Friend_List.objects.filter(user_id=username,friend_id=frnd) | Friend_List.objects.filter(user_id=frnd,friend_id=username)
            print('reject')
            print(frndObj)
            obj = frndObj.first()
            obj.delete()

    frndReqList = Friend_List.objects.filter(user_id=username,friend_status='pending') | Friend_List.objects.filter(friend_id=username,friend_status='pending')
    return render(request,'notification.html',{'frndReqList':frndReqList,'user':username})


def store(request):
    if request.session.get('username') is None:
        return redirect('login')

    if request.method == 'POST':
        username = request.session.get('username')
        friend = request.POST.get('friend')
        print(friend)
        user_id = User.objects.get(user_id=username)
        friend_id = User.objects.get(user_id=friend)
 
        obj = Friend_List.objects.create(user_id=user_id,friend_id=friend_id,friend_since=date.today(),friend_status='pending')
        obj.save()
        return redirect('store')
    else :
        username = request.session.get('username')
        # print(username)
        user_obj_list = User.objects.all()

        sent_frnd_obj_list = Friend_List.objects.filter(user_id=username,friend_status='pending') | Friend_List.objects.filter(friend_id=username,friend_status='pending')

        accept_frnd_obj_list = Friend_List.objects.filter(user_id=username,friend_status='accept') | Friend_List.objects.filter(friend_id=username,friend_status='accept')

        userObj = User.objects.get(username=username)

        all_user_list = []
        admin = 'a1' 
        for user in user_obj_list:
            if user.username != username and user.username != admin:
                all_user_list.append(user.username)

        print("all_user_list:")
        print(all_user_list)

        accept_user_list = []

        for user in accept_frnd_obj_list:
            if user.user_id != userObj:
                accept_user_list.append(user.user_id.username)
            else:
                accept_user_list.append(user.friend_id.username)

        sent_user_list = []

        for user in sent_frnd_obj_list:
            if user.user_id != userObj:
                sent_user_list.append(user.user_id.username)
            else:
                sent_user_list.append(user.friend_id.username)
        
        final_list = []

        for u in all_user_list:
            if u not in accept_user_list:
                final_list.append(u)

        print("final_list:")
        print(final_list)

        print("sent_user_list:")
        print(sent_user_list)

        print("accept_user_list:")
        print(accept_user_list)

        return render(request,'store.html',{'userList':final_list,'sentList':sent_user_list,'user':username})

def logout(request):
    return redirect('login')

def index(request):
    if request.session.get('username') != None:
        username = request.session.get('username')
        friend_id = username
        frndlist = Friend_List.objects.filter(user_id=username,friend_status='accept') | Friend_List.objects.filter(friend_id=username,friend_status='accept')
        sortfrndlist = frndlist.order_by('-last_chat_date')
        return render(request,'index.html',{'frndlist':sortfrndlist,'user':username,'frnd':friend_id,'today_date':date.today(),'yesterday_date':date.today()-timedelta(days=1)})
    else:
        return redirect('login')

def chatWithFriend(request,friend_id):
    if request.session.get('username') is None:
        return redirect('login')

    print('chatWithFriend '+friend_id)
    username = request.session.get('username')
    print(username)

    chats = Chats.objects.filter(sender_id=friend_id,receiver_id=username) | Chats.objects.filter(sender_id=username,receiver_id=friend_id)
    sortchats = chats.order_by('msg_date','msg_time')

    request.session['friend']=friend_id
    frndlist = Friend_List.objects.filter(user_id=username,friend_status='accept') | Friend_List.objects.filter(friend_id=username,friend_status='accept')
    sortfrndlist = frndlist.order_by('-last_chat_date')
    print(date.today()-timedelta(days=1))
    return render(request,'index.html',{'chats':sortchats,'user':username,'frnd':friend_id,'frndlist':sortfrndlist,'today_date':date.today(),'yesterday_date':date.today()-timedelta(days=1)})

def sendMsg(request):
    if request.session.get('username') is None:
        return redirect('login')

    friend_id =  request.session.get('friend')
    username = request.session.get('username')

    # print("username")
    userObj = User.objects.get(username=username)
    frndObj = User.objects.get(username=friend_id)

    frndlistObj = Friend_List.objects.get(Q(friend_id=frndObj,user_id=userObj)|Q(friend_id=userObj,user_id=frndObj))
    frndlistObj.last_chat_time = datetime.now().strftime("%H:%M")
    frndlistObj.last_chat_date = date.today()
    frndlistObj.save()

    msg = request.POST['msg']

    chat = Chats.objects.create(sender_id=userObj,receiver_id=frndObj,msg=msg,msg_time=datetime.now().strftime("%H:%M"),msg_date=date.today())
    chat.save()
    print(username)
    print(friend_id)
    print(msg)

    chats = Chats.objects.filter(sender_id=friend_id,receiver_id=username) | Chats.objects.filter(sender_id=username,receiver_id=friend_id)
    sortchats = chats.order_by('msg_time','msg_date')

    frndlist = Friend_List.objects.filter(user_id=username,friend_status='accept') | Friend_List.objects.filter(friend_id=username,friend_status='accept')
    sortfrndlist = frndlist.order_by('-last_chat_date','-last_chat_time')
    return render(request,'index.html',{'chats':sortchats,'user':username,'frnd':friend_id,'frndlist':sortfrndlist,'today_date':date.today()})