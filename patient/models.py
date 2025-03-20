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
    username = StringField()
    password = StringField()
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
    patient_type = fields.StringField()
    diagonised_on = fields.DateTimeField()
    notes = fields.StringField()
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
    specialization = fields.StringField() 
    working_hours = MapField(ListField(StringField()))
    created_at = fields.DateTimeField()
   
    meta = {'collection':'doctors'}
    
    
class ProfessionalUserGroup(Document):
    professional = ReferenceField(Professional)
    group_head = ReferenceField(ProfessionalUser) # new
    name = StringField()
    description = StringField()
    created = DateTimeField()
    role = StringField()
    acls = DictField()    