from django import forms
from django.core.validators import FileExtensionValidator
from bootstrap_datepicker_plus.widgets import DatePickerInput

from .models import SupplyChainDueDiligence

import utils.form_style as form_style
class DueDiligenceInsertForm(forms.ModelForm):
    class Meta:
        model = SupplyChainDueDiligence
        fields = ["supply_chain_due_diligence_report", "third_party_assurances", "supply_chain_indices"]
    
    supply_chain_due_diligence_report = forms.FileField(widget=form_style.file_input, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    third_party_assurances = forms.FileField(widget=form_style.file_input, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    supply_chain_indices = forms.FloatField(widget=form_style.number_input)
    
class DueDiligenceUpdateForm(DueDiligenceInsertForm):
    class Meta:
        model = SupplyChainDueDiligence
        fields = ["supply_chain_due_diligence_report", "third_party_assurances", "supply_chain_indices"]
        
    supply_chain_due_diligence_report = forms.FileField(required=False, widget=form_style.file_input, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    third_party_assurances = forms.FileField(required=False, widget=form_style.file_input, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    supply_chain_indices = forms.FloatField(widget=form_style.number_input)
    
class DateFilterForm(forms.Form):
    start_date = forms.DateField(label="Start Date",widget=form_style.date_input,required=False,)
    end_date = forms.DateField(label="End Date",widget=DatePickerInput(range_from='start_date', options={'locale': 'en', 'format': 'DD/MM/YYYY'}, attrs=form_style.date_input_style),required=False,)
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("End date must be after start date.")

        return cleaned_data