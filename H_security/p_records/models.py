from django.db import models
from .choices import *
from django.contrib.auth import get_user_model
from djmoney.models.fields import MoneyField
User = get_user_model()

# Create your models here.

class LabTest(models.Model):
    test = models.CharField(max_length=100)
    medical_images = models.ImageField(upload_to='medical_images')
    finding = models.TextField(max_length=1000)
    
    def __str__(self):
        return self.test
    
class Diagnosis(models.Model):
    diagnosis = models.CharField(max_length=500)
    
    def __str__(self):
        return self.diagnosis
    
    class Meta:
        verbose_name = "Diagnosis"
    
class Prescription(models.Model):
    prescription_type = models.CharField(choices=PRESCRIPTION_TYPE, max_length=100)
    medicine_type = models.CharField(choices=MEDICINE_TYPE, max_length=100)
    medicine_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.medicine_name
    
class Bill(models.Model):
    consultation = MoneyField(max_digits=14, decimal_places=2, default_currency='KES', default=('0.0'))
    lab_tests = MoneyField(max_digits=14, decimal_places=2, default_currency='KES', default=('0.0'))
    medical_imaging = MoneyField(max_digits=14, decimal_places=2, default_currency='KES', default=('0.0'))
    medicine = MoneyField(max_digits=14, decimal_places=2, default_currency='KES', default=('0.0'))
    treatment = MoneyField(max_digits=14, decimal_places=2, default_currency='KES', default=('0.0'))
    surgery = MoneyField(max_digits=14, decimal_places=2, default_currency='KES', default=('0.0'))
    billed_to = models.CharField(choices=PAYMENT_OPTIONS, max_length=100)
    paid = models.BooleanField(default=False)
    
    def __str__(self):
        return (self.consultation + self.lab_tests + self.medical_imaging + self.medicine + self.treatment + self.surgery)

class HospitalVisit(models.Model):
    tests = models.ManyToManyField(LabTest, related_name="h_tests")
    diagnosis = models.ManyToManyField(Diagnosis, related_name="h_diagnosis")
    prescriptions = models.ManyToManyField(Prescription, related_name="h_prescriptions")
    edited_by = models.ManyToManyField(User, related_name="h_edited_by")
    date_recorded = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.date_recorded
    
    def hospitals(self):
        if self.edited_by:
            hospitals = []
            for x in self.edited_by:
                hospitals.append(x)
        return set(hospitals)
        
    
class PreexistingCondition(models.Model):
    condition = models.CharField(max_length=200)
    
    def __str__(self):
        return self.condition
    
class HealthRecord(models.Model):
    owner = models.ForeignKey(User, on_delete= models.CASCADE)
    pre_existing_conditions = models.ManyToManyField(PreexistingCondition, related_name="h_pre_conditions")
    hospital_visits = models.ManyToManyField(HospitalVisit, related_name="h_hospital_visits")
    
    def __str__(self):
        return self.owner