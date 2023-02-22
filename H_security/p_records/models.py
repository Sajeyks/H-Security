from django.db import models
from .choices import *
from django.contrib.auth import get_user_model
from djmoney.models.fields import MoneyField
User = get_user_model()

# Create your models here.

class HospitalVisit(models.Model):
    tests = models.TextField(max_length=200, blank=True)
    diagnosis = models.TextField(max_length=200, blank=True)
    prescriptions = models.TextField(max_length=200, blank=True)
    edited_by = models.ManyToManyField(User, related_name="h_edited_by", blank=True)
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
    owner = models.ForeignKey(User, on_delete= models.CASCADE)
    pre_existing_conditions = models.TextField(max_length=200, blank=True)
    hospital_visits = models.ManyToManyField(HospitalVisit, related_name="h_hospital_visits")
    
    def __str__(self):
        return str(self.owner)