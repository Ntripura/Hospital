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
            
            user = models.HospitalModel(name=hname,chairperson=ceo,
                                        country=country,email=email_data.lower(),
                                        mobile=mobile_data,hid=h_id,username=username,password=password,
                                        confirm_password=confirm_password,
                                        password_hash=hash_password
                                )
            user.save()
           
            return JsonResponse({'error': 'false', 'msg': 'User created successfully'})
        
        return JsonResponse({'error': 'true', 'msg': 'User creation failed', 'form': form.errors})


class Login(View):
    form = forms.LoginForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(Login, self).dispatch(request, *args, **kwargs)
    
    
    @validate_payload
    def post(self, request):
        account = 'professional'
        resp = db.user_login(account, self.payload)
        if resp["error"]:
            return JsonResponse(resp)
        payload = {'uid': self.payload['hid'], 'account': account}
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return JsonResponse({'error': False, 'token': token.decode()})


    # def post(self, request):
    #     data = json.loads(request.body.decode('utf-8'))
    #     form = forms.LoginForm(data)
    #     if form.is_valid():
    #         username = form.cleaned_data['username']
    #         password = form.cleaned_data['password']
           
    #         user = models.HospitalModel.objects.filter(username=username).first()
    #         if user and check_password(password, user.password_hash):
    #             id = str(user.id)
    #             hid = user.hid
    #             payload = {
    #                 "username": user.username,
    #                 "id": id,
    #                 "hospitalid": hid,
    #                 'exp': datetime.now(timezone.utc) + timedelta(seconds=300)
    #             }
    #             SECRET = settings.SECRET_KEY
    #             token = jwt.encode(payload, SECRET, algorithm='HS256')
    #             return JsonResponse({'error': 'false', 'token': token.decode("utf-8")})
            
    #         return JsonResponse({'error': 'true', 'msg': 'Invalid username or password'})

    #     return JsonResponse({'error': 'true', 'msg': 'Login failed', 'form': form.errors})
    
    
    