import json
from datetime import datetime, timedelta
import hashlib

from django.contrib.auth import hashers
from patient.models import HospitalModel, PatientModel, DoctorModel,HospitalUserGroup

import logging

logger = logging.getLogger()

# def user_login(username,password):
#     #h = HospitalModel.objects.filter(username=data['username'], hid=data['hid']).first()
#     # h = HospitalUserGroup.objects(username=data['username'],hospital=data['hospital']).first()
#     h = HospitalUserGroup.objects(username=data['username']).first()
#     if h:
#         if hashers.check_password(data['password'], h.password):
#             return {'error': False, 'account_id': h.hospital}
#         return {'error': True, 'msg': 'Invalid password'}
#     return {'error': True, 'msg': 'Account not found.'}


# def get_role():
#     admin = HospitalUserGroup.objects(professional=user.hospital, name="admin").first()
#     doc = HospitalUserGroup.objects(professional=user.doctor, name="doctor").first()
#     pat = HospitalUserGroup.objects(professional=user.patient, name="patient").first()