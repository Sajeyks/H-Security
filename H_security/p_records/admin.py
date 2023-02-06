from django.contrib import admin
from .models import LabTest, Diagnosis, Prescription, PreexistingCondition, HealthRecord, HospitalVisit, Bill
# Register your models here.

admin.site.register(LabTest)
admin.site.register(Diagnosis)
admin.site.register(Prescription)
admin.site.register(PreexistingCondition)
admin.site.register(HealthRecord)
admin.site.register(HospitalVisit)
admin.site.register(Bill)
