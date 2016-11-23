from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from models import User 
from models import Friendships 

import datetime

def index(request):
    return render(request, 'belt_app/index.html')
    
    
def register(request):
    if request.method =='POST':
        
        d = datetime.datetime.strptime
        myDateOfBirth = request.POST['dob']
        print myDateOfBirth
        mydate = d(myDateOfBirth,'%Y-%m-%d').date()
        print mydate
        result= User.objects.register(alias=request.POST['alias'], first_name =request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=request.POST['password'],conf_password=request.POST['conf_password'], dob=request.POST['dob'])
        print '***',result, '***'
        if result[0]:
            request.session['errors_list']=[]
            request.session['user_id'] = result[1]
            print request.session['user_id']
            users= User.objects.all()
            return redirect(reverse('home'))
        else:
            request.session['errors_list'] = result[1]
            return redirect(reverse('index'))
            
    else:
        print 'no post'
        
def login(request):
    if request.method =='POST':
        result= User.objects.login(email=request.POST['email'], password=request.POST['password'])
        print '***',result, '***'
        if result[0]:
            request.session['errors_log_list']=[]
            request.session['email'] = request.POST['email']
            request.session['user_id'] = result[1]
            users= User.objects.all()
            return redirect(reverse('home'))
        else:
            request.session['errors_log_list'] = result[1]
            return redirect(reverse('index'))
            
def home(request):    
    users= User.objects.all()
    print '***',request.session['user_id']
    this_user = User.objects.get(id=request.session['user_id'])
    print this_user.first_name
    other_users= User.objects.filter(id__lte=this_user.id)|User.objects.filter(id__gte=this_user.id)
    friends = Friendships.objects.filter(user__id=this_user.id).distinct()
    
    users_to_exclude = Friendships.objects.filter(user__id=this_user.id)
    
    names_to_exclude = [f.friend.id for f in friends] 
    
    notfriends = User.objects.exclude(id__in=names_to_exclude).exclude(id=this_user.id)
    
    
    print '***************users_to_exclude***'
    for friend in users_to_exclude:
        print friend.user.id, friend.friend_id, friend.friend.first_name
    
    
    
    
    print '***************Friends***'
    for friend in friends:
        print friend.user.id, friend.friend_id, friend.friend.first_name
    
    
    print '***************NOt Friends***'
    for user in notfriends:
        print user.id, user.first_name
    print other_users
    
    
    context = {
               'this_user': this_user,
               'other_users':notfriends,
               'friends':friends
                }
    return render(request, 'belt_app/home.html', context)
    
def friendships(request, friendid):
    if request.method =='POST':
        user_id = request.session['user_id']
        print '********************',user_id , friendid
        
        this_user = User.objects.get(id=user_id)
        this_friend = User.objects.get(id=friendid)
        
        result= Friendships.objects.addfriendship(user=this_user, friend =this_friend)
        
        if result[0]:
            print result[1]
        else:
            print 'FAIL'
            return redirect(reverse('index'))            
    return redirect(reverse('home'))
    
def show_user(request, user_id):
    this_user = User.objects.get(id=user_id)
    user_id = this_user.id

    context = {
               'this_user': this_user,
               'user_id': user_id
                }
    return render(request, 'belt_app/user.html', context)
    
    
def remove_asfriend(request, friendid):
    this_friendship = Friendships.objects.get(id=friendid)
    h = Friendships.objects.get(id=friendid).delete()

    context = {
               'this_user': this_friendship
                }
    return redirect(reverse('home'))