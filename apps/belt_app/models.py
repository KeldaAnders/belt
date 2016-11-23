from __future__ import unicode_literals
import bcrypt, re
EMAIL_REGEX = re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')
from django.db import models 
import datetime

class UserManager(models.Manager):
    def register(self, **kwargs):
        # errors=False
        errors_list = []
        d = datetime.datetime.strptime
        if len(kwargs['alias']) is 0:
            errors_list.append('User name is required')
            # errors = True
            
        if len(kwargs['first_name']) < 2:
            errors_list.append('First Name is required')
            # errors = True
        if not kwargs['first_name'].isalpha():
            errors_list.append('First Name must only contain letters')
            # errors = True
        if len(kwargs['first_name']) < 2:
            errors_list.append('Last Name is required')
            # errors = True
            
        if not kwargs['last_name'].isalpha():
            errors_list.append('Last Name must only contain letters')
            # errors = True
        
        if len(kwargs['email']) < 5:
            errors_list.append('Email is required')
            # errors = True
            
        if not EMAIL_REGEX.match(kwargs['email']):
            errors_list.append('Email must be a valid email')
            # errors = True
        try:
            d(kwargs['dob'], "%Y-%m-%d")
            if d(kwargs['dob'], "%Y-%m-%d") >= datetime.datetime.today():
                    errors_list.append("You are not born yet, please enter a valid Date of Birth")

        except:
            errors_list.append('Not a valid birthday')

        
        if not re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', kwargs['password']):
            errors_list.append('Password must contain 8 characters and at least one number, one letter and one unique character such as @#$%^&+=')
            # errors = True
        if not kwargs['password'] == kwargs['conf_password']:
            errors_list.append('Password and conformation must match')
            # errors = True
            
        if len(errors_list) is 0:
            pw_hash = bcrypt.hashpw(kwargs['password'].encode(), bcrypt.gensalt())
            print pw_hash, kwargs['password'], '*'*85
            user= self.create(alias=kwargs['alias'],first_name = kwargs['first_name'],last_name = kwargs['last_name'], email=kwargs['email'],password = pw_hash,dob=kwargs['dob'])
            print user.id 
            return (True ,user.id)
        else:
            print errors_list
            return (False, errors_list)

    def login(self, **kwargs):
        errors_log_list = []
        
        if len(kwargs['email']) < 5:
            errors_log_list.append('Email is required')
            # errors = True
            
        if not EMAIL_REGEX.match(kwargs['email']):
            errors_log_list.append('Email must be a valid email')
            # errors = True
        if len(errors_log_list) is 0:
            try:
                print "in user block"
                user = User.objects.get(email=kwargs['email'])
                print user.id, user.email
                input_pw = kwargs['password'].encode()
                hashed_pw = user.password.encode()
                print input_pw, hashed_pw,'.'*85
                if bcrypt.hashpw(input_pw, hashed_pw) == hashed_pw:
                    
                    print user.id, "hey ya"
                    return (True ,user.id)
                
            except:
                errors_log_list.append('No user with matching username and password')
                return (False, errors_log_list)
        else:
            return (False, errors_log_list)
            
            
class User(models.Model):
    email = models.CharField(max_length=255)
    alias = models.CharField(max_length=45)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    dob = models.DateField()
    password = models.CharField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
#     


class FriendshipManager(models.Manager):
    def addfriendship(self, **kwargs):
        errors_review_list = []

        if len(errors_review_list) is 0:
            friendship = self.create(user=kwargs['user'],friend = kwargs['friend'])
            print friendship.id
            return (True, friendship.id)
        else:
            return (False, errors_review_list)
    
    
class Friendships(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, related_name="userfriendship")
    friend = models.ForeignKey('User', models.DO_NOTHING, related_name ="friendsfriendship")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = FriendshipManager()
            
    