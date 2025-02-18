from django import forms
from django.core.validators import FileExtensionValidator

from .models import SupplyChainDueDiligence

from utils.validators import validate_pdf_file

class DueDiligenceForm(forms.ModelForm):
    class Meta:
        model = SupplyChainDueDiligence
        fields = ["supply_chain_due_diligence_report", "third_party_assurances", "supply_chain_indices"]
    
    input_style = {"class": "form-control mt-2"}
    text_input = forms.FileInput(attrs=input_style) 
    
    supply_chain_due_diligence_report = forms.FileField(widget=text_input, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    third_party_assurances = forms.FileField(widget=text_input, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    supply_chain_indices = forms.FloatField(widget=forms.NumberInput(attrs=input_style))