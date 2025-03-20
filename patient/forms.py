from django import forms
from datetime import datetime
from patient import models
from django.core.exceptions import ValidationError
from django.http import JsonResponse


class LoginForm(forms.Form):
      username = forms.CharField()
      password = forms.CharField()
      userid = forms.CharField(required=False)



# class ProfessionalLoginForm(forms.Form):
#     email = forms.EmailField()
#     password = forms.CharField()
#     plan = forms.CharField(required=False)
#     userid = forms.CharField(required=False)

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
     