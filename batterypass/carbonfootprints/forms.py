from django import forms
from django.core.validators import FileExtensionValidator

from .models import CarbonFootprintPerLifecycleStageEntity, CarbonFootprintForBatteries

from dal import autocomplete

from utils.upload_util import Upload
from .const import carbon_footprint_study_path

from datetime import datetime

import utils.form_style as form_style
import utils.validators as validators

import traceback

class CarbonFootprintsLifecycleForm(forms.ModelForm):
    class Meta:
        model = CarbonFootprintPerLifecycleStageEntity
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(form_style.input_style)
    
class CFForBatteriesInsertForm(forms.ModelForm):
    class Meta:
        model = CarbonFootprintForBatteries
        fields = '__all__'
        widgets = {
            'carbon_footprint_per_lifecycle_stage': autocomplete.ModelSelect2Multiple(url='cfperlifecyclese-autocomplete', attrs=form_style.input_style)
        }
        
    carbon_footprint_study = forms.FileField(widget=form_style.file_input, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(form_style.input_style)
    
    def save(self, commit=True):
        instance = super(CFForBatteriesInsertForm, self).save(commit=False)
        try:
            instance.carbon_footprint_study = Upload.handle_single_upload(
                carbon_footprint_study_path, 
                self.cleaned_data['carbon_footprint_study'], 
                f'carbon_footprint_study_{datetime.now().timestamp()}')
            print(instance.carbon_footprint_study)
            if commit:
                instance.save()
                instance.carbon_footprint_per_lifecycle_stage.set(self.cleaned_data['carbon_footprint_per_lifecycle_stage'])
        except Exception as exception:
            tb = traceback.format_exc()
            print(f"errors : {exception}\ntrace : {tb}")
        return instance

class CFForBatteriesUpdateForm(forms.ModelForm):
    class Meta:
        model = CarbonFootprintForBatteries
        fields = '__all__'
        widgets = {
            'carbon_footprint_per_lifecycle_stage': autocomplete.ModelSelect2Multiple(url='cfperlifecyclese-autocomplete', attrs=form_style.input_style)
        }
        
    carbon_footprint_study = forms.FileField(widget=form_style.file_input, required=False, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(form_style.input_style)
    
    def save(self, commit=True):
        instance = super(CFForBatteriesUpdateForm, self).save(commit=False)
        try:
            print(self.cleaned_data['carbon_footprint_study'])
            if self.files.keys() >= {'carbon_footprint_study'}:
                #remove old file
                Upload.remove_files([f'{carbon_footprint_study_path}/{instance.carbon_footprint_study}'])
                #upload new file
                instance.carbon_footprint_study = Upload.handle_single_upload(
                    carbon_footprint_study_path, 
                    self.cleaned_data['carbon_footprint_study'], 
                    f'carbon_footprint_study_{datetime.now().timestamp()}')
            if commit:
                instance.save()
                instance.carbon_footprint_per_lifecycle_stage.set(self.cleaned_data['carbon_footprint_per_lifecycle_stage'])
        except Exception as exception:
            tb = traceback.format_exc()
            print(f"errors : {exception}\ntrace : {tb}")
        return instance
            
