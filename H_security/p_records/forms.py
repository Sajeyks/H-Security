from django import forms
from .models import HealthRecord, HospitalVisit
from .choices import *

class UpdatePreconditionsForm(forms.ModelForm):
    
    class Meta:
        model = HealthRecord
        fields = ['pre_existing_conditions']
        
        
class HospitalVisitForm(forms.ModelForm):
    
    billed_to = forms.ChoiceField(choices=PAYMENT_OPTIONS, widget=forms.RadioSelect)
    paid = forms.BooleanField(required=False, widget=forms.CheckboxInput)
    
    
    class Meta:
        model = HospitalVisit
        fields = ["tests", "diagnosis", "prescriptions", "bill", "billed_to", "paid"]
    