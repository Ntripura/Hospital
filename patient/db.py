import json
from datetime import datetime, timedelta
import hashlib

from django.contrib.auth import hashers
from patient.models import HospitalModel, PatientModel, DoctorModel

import logging

logger = logging.getLogger()




def user_login(account, data):
    h = HospitalModel.objects(username=account, hid=data['hid']).first()
    if h:
        if hashers.check_password(data['password'], h.password):
            return {'error': False, 'account_id': h.id}
        return {'error': True, 'msg': 'Invalid password'}
    return {'error': True, 'msg': 'Account not found.'}