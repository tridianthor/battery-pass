from django import forms
from django.core.validators import FileExtensionValidator

from .models import SupplyChainDueDiligence

import utils.form_style as form_style

class DueDiligenceForm(forms.ModelForm):
    class Meta:
        model = SupplyChainDueDiligence
        fields = ["supply_chain_due_diligence_report", "third_party_assurances", "supply_chain_indices"]
    
    supply_chain_due_diligence_report = forms.FileField(widget=form_style.file_input, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    third_party_assurances = forms.FileField(widget=form_style.file_input, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    supply_chain_indices = forms.FloatField(widget=form_style.number_input)