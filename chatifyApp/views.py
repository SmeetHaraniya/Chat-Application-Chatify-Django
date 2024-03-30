from django.shortcuts import render,redirect
from django.http import HttpResponse

from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import User,Themes, Friend_List, Groups, Group_Members, Chats, Group_chat

from django.utils import timezone
from datetime import datetime,date

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
            # return render(request,'index.html')
            request.session['username'] = username
            return redirect('index')
        else:
            messages.info(request,'Invalid credential')
            return render(request,'login.html')
    else:
        print('notpost')    
        return render(request,'login.html')


def signup(request):
    if request.method == 'POST':
        # return render(request,'login.html')
        
        firstname = request.POST['firstName']
        lastname = request.POST['lastName']
        dob = request.POST['dob']
        phoneno = request.POST['phoneNo']
        username = request.POST['userName']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if password==cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username already exists")
                print("username exist")
                return redirect('signup')
            elif User.objects.filter(phoneno=phoneno).exists():
                messages.info(request,"MobileNo already exists")
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
            messages.info(request,'Password not matching')
            print("passwrod not match")
            return redirect('signup')
    else:
        return render(request,'signup.html')

def setting(request):
    username = request.session.get('username')
    return render(request,'setting.html',{'username':username})

def notification(request):
    username = request.session.get('username')
    print(request.method)
    if request.method == 'POST':
        print("username")
        frnd = request.POST.get('frnd')
        print(frnd)
        try :
            frndObj = Friend_List.objects.filter(user_id=username,friend_id=frnd) | Friend_List.objects.filter(user_id=frnd,friend_id=username)
            obj = frndObj.first()
            # print("obj")
            # print(obj)
            obj.friend_status = "accept"
            obj.save()
        except Exception as e:
            print(e)
        print(frnd)
    print("Helloo")
    frndReqList = Friend_List.objects.filter(user_id=username,friend_status='pending') | Friend_List.objects.filter(friend_id=username,friend_status='pending')
    return render(request,'notification.html',{'frndReqList':frndReqList,'user':username})
    # return render(request,'notification.html')

def store(request):
    if request.method == 'POST':
        username = request.session.get('username')
        friend = request.POST.get('friend')

        user_id = User.objects.get(user_id=username)
        friend_id = User.objects.get(user_id=friend)
 
        obj = Friend_List.objects.create(user_id=user_id,friend_id=friend_id,friend_since=date.today(),friend_status='pending')
        obj.save()

    username = request.session.get('username')
    print(username)
    user_obj_list = User.objects.all()
    frnd_obj_list = Friend_List.objects.filter(user_id=username,friend_status='pending') | Friend_List.objects.filter(friend_id=username,friend_status='pending')

    userobj = User.objects.get(username=username)

    frnd_list = []
    user_list = []

    for frnd in frnd_obj_list:
        if userobj == frnd.user_id:
            frnd_list.append(frnd.friend_id.username)
        else:
            frnd_list.append(frnd.user_id.username)

    for user in user_obj_list:
        if user.username != username:
            user_list.append(user.username)
    
    print(frnd_list)
    print(user_list)
    return render(request,'store.html',{'userList':user_list,'frndList':frnd_list,'user':username})

def logout(request):
    return redirect('login')

def index(request):
    if request.session.get('username') != None:
        username = request.session.get('username')
        friend_id = username
        frndlist = Friend_List.objects.filter(user_id=username,friend_status='accept') | Friend_List.objects.filter(friend_id=username,friend_status='accept')
        return render(request,'index.html',{'frndlist':frndlist,'user':username,'frnd':friend_id})
    else:
        return redirect('login')

def chatWithFriend(request,friend_id):
    print('chatWithFriend '+friend_id);
    username = request.session.get('username')
    print(username)
    chats = Chats.objects.filter(sender_id=friend_id,receiver_id=username) | Chats.objects.filter(sender_id=username,receiver_id=friend_id)
    sortchats = chats.order_by('msg_date','msg_time')

    request.session['friend']=friend_id
    frndlist = Friend_List.objects.filter(user_id=username,friend_status='accept') | Friend_List.objects.filter(friend_id=username,friend_status='accept')
    
    return render(request,'index.html',{'chats':sortchats,'user':username,'frnd':friend_id,'frndlist':frndlist})

def sendMsg(request):
    friend_id =  request.session.get('friend')
    username = request.session.get('username')
    msg = request.POST['msg']

    userObj = User.objects.get(username=username)
    frndObj = User.objects.get(username=friend_id)

    chat = Chats.objects.create(sender_id=userObj,receiver_id=frndObj,msg=msg,msg_time=datetime.now().strftime("%H:%M"),msg_date=date.today())
    chat.save()
    print(username)
    print(friend_id)
    print(msg)

    chats = Chats.objects.filter(sender_id=friend_id,receiver_id=username) | Chats.objects.filter(sender_id=username,receiver_id=friend_id)
    sortchats = chats.order_by('msg_time','msg_date')

    frndlist = Friend_List.objects.filter(user_id=username,friend_status='accept') | Friend_List.objects.filter(friend_id=username,friend_status='accept')
    
    return render(request,'index.html',{'chats':sortchats,'user':username,'frnd':friend_id,'frndlist':frndlist})