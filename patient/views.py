from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views import View  
from django import forms
from patient import models
from patient import forms
from patient import db
#from consumer import db
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta, datetime, timezone
from Hospital.auth import authenticate, validate_payload
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
import json
import jwt
import os
import logging

class Register(View):
    form = forms.HospitalForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(Register, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        form = forms.HospitalForm(data)
        
        if form.is_valid():
            hname = form.cleaned_data['name']
            ceo = form.cleaned_data['chairperson']
            country = form.cleaned_data['country']
            mobile_data = form.cleaned_data['mobile']
            email_data = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            h_id = os.urandom(8).hex().upper()
            if password != confirm_password:
                return JsonResponse({'error': 'true', 'msg': 'Passwords do not match'})
            hash_password = make_password(password)
            
            h = models.HospitalModel(name=hname,chairperson=ceo,
                                        country=country,email=email_data.lower(),
                                        mobile=mobile_data,hid=h_id,username=username,password=password,
                                        confirm_password=confirm_password,
                                        password_hash=hash_password
                                )
            h.save()
            admin = models.HospitalUserGroup(username=username,password=password,
                                             password_hash=hash_password,
                                role="admin", hospital=h,isadmin=True
                                )
            admin.save()
            logging.info('Admin created successfully')
            return JsonResponse({'error': 'false', 'msg': 'User created successfully'})
        
        return JsonResponse({'error': 'true', 'msg': 'User creation failed', 'form': form.errors})


class Login(View):
    form = forms.LoginForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(Login, self).dispatch(request, *args, **kwargs)
    
    
    # @validate_payload
    # def post(self, request):
    #     username = self.payload.get('username')
    #     password = self.payload.get('password')
    #     #resp = db.user_login( self.payload)
    #     resp = db.user_login( username,self.payload)
       
    #     if resp["error"]:
    #         return JsonResponse(resp)
    #     user = resp["user"]
    #     payload = {'hid': user.hospital, 'username':user.username,'role':user.role}
    #     token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    #     user.last_login = datetime.now()
    #     user.save()
    #     return JsonResponse({'error': False, 'token': token.decode()})


    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        form = forms.LoginForm(data)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
           
            hos = models.HospitalModel.objects.filter(username=username).first()
            huser = models.HospitalUserGroup.objects.filter(username=username).first()
            if hos.username == huser.username and check_password(password,huser.password_hash):
           # if user and password1==user.password:
             
                id = str(hos.id)
               # hospitalid=str(huser.hospital) if huser.hospital else None

                print(id)
              #  print(hospitalid)
                payload = {
                    "username": hos.username,
                    "id": id,
                    "role":huser.role,
                    'exp': datetime.now(timezone.utc) + timedelta(seconds=1800)
                }
                SECRET = settings.SECRET_KEY
                token = jwt.encode(payload, SECRET, algorithm='HS256')
                return JsonResponse({'error': 'false', 'token': token.decode("utf-8")})
            
            return JsonResponse({'error': 'true', 'msg': 'Invalid username or password'})

        return JsonResponse({'error': 'true', 'msg': 'Login failed', 'form': form.errors})
    
    
class DoctorDetails(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(DoctorDetails, self).dispatch(request, *args, **kwargs)
    
    @authenticate
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        form = forms.DoctorCreateForm(data)
        
        if form.is_valid():
            fname = form.cleaned_data['first_name']
            lname = form.cleaned_data['last_name']
            contry = form.cleaned_data['country']
            gen = form.cleaned_data['gender']
            dob = form.cleaned_data['dob']
            mob = form.cleaned_data['mobile']
            em = form.cleaned_data['email']
            uname = form.cleaned_data['username']
            pswd = form.cleaned_data['password']
            spzn = form.cleaned_data['specialization']
            lno = form.cleaned_data['license_number']
            exp = form.cleaned_data['experience']
            whours = form.cleaned_data['working_hours']
            now = datetime.now(timezone.utc)
            time =now.strftime("%Y-%m-%d %H:%M:%S")
            hash_password = make_password(pswd)
            con = request.user['id']
            doc = models.DoctorModel(hospital = con,first_name =fname, last_name = lname,
                                     country = contry, gender = gen,dob = dob,mobile = mob,email = em,
                                     username = uname,password = pswd,specialization = spzn, 
                                     license_number = lno,experience=exp,
                                     working_hours=whours,created_at=time)     
                     
            doc.save()
            hos = models.HospitalUserGroup(hospital = con,doctor_id = doc,
                                           username = doc.username,password = doc.password,
                                           password_hash = hash_password, created = doc.created_at,
                                           isadmin = False, role = 'doctor'
                                           )
            hos.save()
  
            return JsonResponse({'error': 'false', 'msg': 'Doctor is created successfully'})
        else:
            return JsonResponse({'error':'true','msg':'Doctor creation failed','form':form.errors})
        
        
class LoginUser(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginUser, self).dispatch(request, *args, **kwargs)
    
    @authenticate
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        form = forms.HospitalUserLoginForm(data)
        
        if form.is_valid():
            uname = form.cleaned_data['username']
            pswd = form.cleaned_data['password']
            roles = form.cleaned_data['role']
            
            huser = models.HospitalUserGroup.objects.filter(username=uname).first()
            if huser.username and check_password(pswd,huser.password_hash):    
                if huser.isadmin==True and roles == huser.role: 
                    return JsonResponse({'error': 'false', 'msg': 'Welcome admin'})
                elif huser.isadmin == False and roles=='doctor':
                    return JsonResponse({'error': 'false', 'msg': 'Welcome doctor'})
                else:
                    return JsonResponse({'error': 'false', 'msg': 'Welcome patient'})
        
            return JsonResponse({'error': 'true', 'msg': 'Invalid username or password'})

        return JsonResponse({'error': 'true', 'msg': 'Login failed', 'form': form.errors})
