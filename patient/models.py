from django.db import models
from mongoengine import *
from mongoengine import Document, fields
from django.utils import timezone
from datetime import datetime


class Address(EmbeddedDocument):
    house_flat_no = StringField()
    street = StringField()
    city_town = StringField()
    state = StringField()
    country = StringField()
    zipcode = StringField()
    

class EmergencyContact(EmbeddedDocument):
    name = StringField()
    relationship = StringField()
    phone = StringField()
    
    
class MedicalHistory(EmbeddedDocument):
   blood_group = fields.StringField()
   diseases = fields.StringField()
   previous_surgery = fields.StringField()
   allergies = StringField()    
   previous_history_notes = fields.StringField()


class HospitalModel(Document):
    name = fields.StringField()
    hid = fields.StringField()
    chairperson = fields.StringField()
    country = fields.StringField()
    mobile = fields.StringField()
    username = fields.StringField()
    password = fields.StringField()
    confirm_password = StringField()
    email = StringField()
    password_hash = fields.StringField()
    
    meta = {'collection': 'hospital'}
    


class PatientModel(Document):  
    hospital = ReferenceField(HospitalModel)
    first_name = fields.StringField()
    last_name = fields.StringField()
    gender = fields.StringField()
    dob = fields.DateTimeField()
    mobile = fields.StringField()
    address = EmbeddedDocumentField(Address)
    email = fields.EmailField()
    password = fields.StringField()
    password_hash = fields.StringField()
    patient_type = fields.StringField()
    medicalhistory = EmbeddedDocumentField(MedicalHistory)
    diagonised_on = fields.DateTimeField()
    visit_date = fields.DateTimeField()
    medication = fields.StringField() 
    dosage = fields.StringField()   
    frequency = fields.StringField()
    instructions = fields.StringField()
    prescribed_date = fields.DateTimeField() 
    emergencycontact = EmbeddedDocumentField(EmergencyContact)
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()
    
    meta = {'collection': 'patient'}
    
    
class DoctorModel(Document):  
    hospital = ReferenceField(HospitalModel)
    first_name = fields.StringField()
    last_name = fields.StringField()
    country = fields.StringField()
    gender = fields.StringField()
    dob = fields.DateTimeField()
    mobile = fields.StringField()
    email = fields.EmailField()
    username = fields.StringField()
    password = fields.StringField()
    password_hash = fields.StringField()
    specialization = fields.StringField() 
    experience = fields.IntField()
    license_number = StringField()
    working_hours = MapField(ListField(StringField()))
    created_at = fields.DateTimeField()
   
    meta = {'collection':'doctors'}
    
    
class HospitalUserGroup(Document):
    hospital = ReferenceField(HospitalModel)
    doctor_id = ReferenceField(DoctorModel) 
    patient_id = ReferenceField(PatientModel) 
    username = StringField()
    password = StringField()
    password_hash = fields.StringField()
    description = StringField()
    created = DateTimeField()
    isadmin = BooleanField(default=False)
    last_login = DateTimeField()
    role = StringField(choices=['admin', 'doctor', 'patient'])
    
    meta = {'collection':'hospitaluser'}
    
    
class AppointmentModel(Document):  
    patient = ReferenceField(PatientModel)
    doctor = ReferenceField(DoctorModel)
    patient_name = fields.StringField()
    appointment_date = fields.DateTimeField()
    patient_mobile = fields.StringField()
    status = fields.StringField(choices=['Scheduled', 'Completed', 'Cancelled'], default='Scheduled') 
    reason = fields.StringField()
    created_on = fields.DateTimeField()
    
    
    meta = {'collection': 'appointment'}
    
