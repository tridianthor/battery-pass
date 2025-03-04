from django import forms
from django.core.validators import FileExtensionValidator

from .models import CarbonFootprintPerLifecycleStageEntity, CarbonFootprintForBatteries

from dal import autocomplete

import utils.form_style as form_style
import utils.validators as validators

class CFPerLifecycleSEForm(forms.ModelForm):
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
            'carbon_footprint_per_lifecycle_stage': autocomplete.ModelSelect2Multiple(url='cfperlifecyclese-autoselect', attrs=form_style.input_style)
        }
        
    carbon_footprint_study = forms.FileField(widget=form_style.file_input, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(form_style.input_style)

class CFForBatteriesUpdateForm(forms.ModelForm):
    class Meta:
        model = CarbonFootprintForBatteries
        fields = '__all__'
        widgets = {
            'carbon_footprint_per_lifecycle_stage': autocomplete.ModelSelect2Multiple(url='cfperlifecyclese-autoselect', attrs=form_style.input_style)
        }
        
    carbon_footprint_study = forms.FileField(widget=form_style.file_input, required=False, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(form_style.input_style)
            
