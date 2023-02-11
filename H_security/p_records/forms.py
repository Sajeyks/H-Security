from django import forms
from .models import HealthRecord

class UpdatePreconditionsForm(forms.ModelForm):
    
    class Meta:
        model = HealthRecord
        fields = ['pre_existing_conditions']
        