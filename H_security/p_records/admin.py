from django.contrib import admin
from .models import HealthRecord, HospitalVisit
# Register your models here.


admin.site.register(HealthRecord)
admin.site.register(HospitalVisit)