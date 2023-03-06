from django.db import models
from .choices import *
from django.contrib.auth import get_user_model
from djmoney.models.fields import MoneyField
User = get_user_model()
from django_cryptography.fields import encrypt

# Create your models here.

class HospitalVisit(models.Model):
    tests = encrypt(models.TextField(max_length=200))
    diagnosis = encrypt(models.TextField(max_length=200))
    prescriptions = encrypt(models.TextField(max_length=200))
    edited_by = models.ManyToManyField(User, related_name="h_edited_by")
    date_recorded = models.DateField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    bill = MoneyField(max_digits=14, decimal_places=2, default_currency='KES', default=('0.0'))
    billed_to = models.CharField(choices=PAYMENT_OPTIONS, max_length=100)
    paid = models.BooleanField(default=False)
    
    
    def __str__(self):
        return str(self.date_recorded)
    
    def hospitals(self):
        if self.edited_by:
            hospitals = []
            for x in self.edited_by:
                hospitals.append(x)
        return set(hospitals)
    
class HealthRecord(models.Model):
    owner = models.OneToOneField(User, on_delete= models.CASCADE)
    pre_existing_conditions = encrypt(models.TextField(max_length=200, blank=True))
    hospital_visits = models.ManyToManyField(HospitalVisit, related_name="h_hospital_visits")
    
    def __str__(self):
        return str(self.owner)
    
    @staticmethod
    def for_group(user):
        if user.groups.filter(name='Hospital Staff Group').exists():
            # user is in allowed_group, return all objects
            return HealthRecord.objects.all()
        elif user.groups.filter(name='Non-Staff Group').exists():
            # user is in restricted_group, return only their own objects
            # return HealthRecord.objects.filter(owner=user)
            return HealthRecord.objects.none()
        else:
            # user is not in either group, return an empty queryset
            return HealthRecord.objects.none()
        
    @staticmethod
    def details_for_group(user, pk):
        if user.groups.filter(name='Hospital Staff Group').exists():
            # user is in allowed_group, return all objects
            return HealthRecord.objects.get(pk=pk)
        elif user.groups.filter(name='Non-Staff Group').exists():
            # user is in restricted_group, return only their own objects
            HealthRecord.objects.none()
        else:
            # user is not in either group, return an empty queryset
            return HospitalVisit.objects.none()