from django import forms
from django.core.validators import FileExtensionValidator

from .models import CarbonFootprintPerLifecycleStageEntity, CarbonFootprintForBatteries

from dal import autocomplete

from utils.upload_util import Upload
from .const import carbon_footprint_study_path

from datetime import datetime

import utils.form as form
import utils.validators as validators

import traceback

class CarbonFootprintsLifecycleForm(forms.ModelForm):
    class Meta:
        model = CarbonFootprintPerLifecycleStageEntity
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(form.input_style)
    
class CFForBatteriesInsertForm(forms.ModelForm):
    class Meta:
        model = CarbonFootprintForBatteries
        fields = '__all__'
        widgets = {
            'carbon_footprint_per_lifecycle_stage': autocomplete.ModelSelect2Multiple(url='cfperlifecyclese-autocomplete', attrs=form.input_style)
        }
        
    carbon_footprint_study = forms.FileField(widget=form.file_input, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(form.input_style)

class CFForBatteriesUpdateForm(forms.ModelForm):
    class Meta:
        model = CarbonFootprintForBatteries
        fields = '__all__'
        widgets = {
            'carbon_footprint_per_lifecycle_stage': autocomplete.ModelSelect2Multiple(url='cfperlifecyclese-autocomplete', attrs=form.input_style)
        }
        
    carbon_footprint_study = forms.FileField(widget=form.file_input, required=False, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(form.input_style)
            
