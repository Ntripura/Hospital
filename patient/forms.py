from django import forms
from datetime import datetime
from patient import models
from django.core.exceptions import ValidationError
from django.http import JsonResponse


class LoginForm(forms.Form):
      username = forms.CharField()
      password = forms.CharField()
      

class HospitalUserLoginForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField(required=False)
    password = forms.CharField()
    role = forms.CharField()


class HospitalForm(forms.Form):
    name = forms.CharField()
    chairperson = forms.CharField()
    country = forms.CharField()
    mobile = forms.CharField()
    username = forms.CharField()
    password = forms.CharField()
    confirm_password = forms.CharField()
    email = forms.EmailField(required=False)
    
    
    def clean_data(self):
        data = super().clean()
        name = data.get('name')
        chairperson = data.get('chairperson')
        email = data.get('email')
        username = data.get('username')
        if not forms.instance:
            if models.HospitalModel.objects.filter(username=username, email=email).exists():
                raise forms.ValidationError('username and email already exists.')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password!= confirm_password:
            raise ValidationError('Invalid password')
     
     
     
class DoctorCreateForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField(required=False)
    country = forms.CharField(required=False)
    gender = forms.CharField()
    dob = forms.DateTimeField(required=False)
    email = forms.EmailField()
    mobile = forms.CharField()
    username = forms.CharField()
    password = forms.CharField()
    specialization = forms.CharField()
    license_number = forms.CharField()
    experience = forms.IntegerField()
    working_hours = forms.JSONField(
        widget=forms.Textarea(attrs={"placeholder": 'Example: {"Monday": ["09:00-12:00", "14:00-18:00"], "Tuesday": ["10:00-16:00"]}'})
    )


class PatientCreateForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField(required=False)
    country = forms.CharField(required=False)
    gender = forms.CharField()
    dob = forms.DateTimeField(required=False)
    email = forms.EmailField()
    mobile = forms.CharField()
    username = forms.CharField()
    password = forms.CharField()
    specialization = forms.CharField()
    license_number = forms.CharField()
    experience = forms.IntegerField()
    working_hours = forms.JSONField(
        widget=forms.Textarea(attrs={"placeholder": 'Example: {"Monday": ["09:00-12:00", "14:00-18:00"], "Tuesday": ["10:00-16:00"]}'})
    )

   
   
   
   