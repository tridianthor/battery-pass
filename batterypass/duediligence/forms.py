from django import forms
from django.core.validators import FileExtensionValidator
from bootstrap_datepicker_plus.widgets import DatePickerInput

from .models import SupplyChainDueDiligence

import utils.form as form
class DueDiligenceInsertForm(forms.ModelForm):
    class Meta:
        model = SupplyChainDueDiligence
        fields = '__all__'
    
    supply_chain_due_diligence_report = forms.FileField(widget=form.file_input, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    third_party_assurances = forms.FileField(widget=form.file_input, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    supply_chain_indices = forms.FloatField(widget=form.number_input)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(form.input_style)
    
class DueDiligenceUpdateForm(DueDiligenceInsertForm):
    class Meta:
        model = SupplyChainDueDiligence
        fields = '__all__'
        
    supply_chain_due_diligence_report = forms.FileField(required=False, widget=form.file_input, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    third_party_assurances = forms.FileField(required=False, widget=form.file_input, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    supply_chain_indices = forms.FloatField(widget=form.number_input)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(form.input_style)
class DateFilterForm(forms.Form):
    start_date = forms.DateField(label="Start Date",widget=form.date_input,required=False,)
    end_date = forms.DateField(label="End Date",widget=DatePickerInput(range_from='start_date', options={'locale': 'en', 'format': 'DD/MM/YYYY'}, attrs=form.date_input_style),required=False,)
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("End date must be after start date.")

        return cleaned_data