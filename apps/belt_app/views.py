from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from models import User


def index(request):
    return render(request, 'belt_app/index.html')
    
    
def register(request):
    if request.method =='POST':
        result= User.objects.register(user_name=request.POST['user_name'], first_name =request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=request.POST['password'],conf_password=request.POST['conf_password'])
        print '***',result, '***'
        if result[0]:
            request.session['errors_list']=[]
            request.session['email'] = request.POST['email']
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
            users= User.objects.all()
            return redirect(reverse('home'))
        else:
            request.session['errors_log_list'] = result[1]
            return redirect(reverse('index'))
            
def home(request):    
    return render(request, 'belt_app/home.html')