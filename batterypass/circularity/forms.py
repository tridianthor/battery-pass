from django import forms
from django.core.validators import FileExtensionValidator

from .models import PostalAddress, ComponentEntity, SparePartSupplierEntity, SafetyMeasuresEntity, RecycledContentEntity, EndOfLifeInformationEntity, DismantlingAndRemovalDocumentation, Circularity

from dal import autocomplete

from utils.upload_util import Upload

from datetime import datetime

import utils.form_style as form_style
import utils.validators as validators

class PostalAddressForm(forms.ModelForm):
    class Meta:
        model = PostalAddress
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(form_style.input_style)

class ComponentEntityForm(forms.ModelForm):
    class Meta:
        model = ComponentEntity
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(form_style.input_style)

class SparePartSupplierEntityForm(forms.ModelForm):
    class Meta:
        model = SparePartSupplierEntity
        fields = '__all__'
        widgets = {
            'components': autocomplete.ModelSelect2Multiple(url='components-autocomplete', attrs=form_style.input_style),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(form_style.input_style)

class SafetyMeasuresEntityInsertForm(forms.ModelForm):
    class Meta:
        model = SafetyMeasuresEntity
        fields = '__all__'
    
    safety_instructions = forms.FileField(widget=form_style.file_input, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    extinguishing_agent = forms.JSONField(widget=form_style.text_area, validators=[validators.validate_json])
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(form_style.input_style)
    
    #TODO override save

class SafetyMeasuresEntityUpdateForm(forms.ModelForm):
    class Meta:
        model = SafetyMeasuresEntity
        fields = '__all__'
    
    safety_instructions = forms.FileField(widget=form_style.file_input, required=False, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    extinguishing_agent = forms.JSONField(widget=form_style.text_area, required=False, validators=[validators.validate_json])
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(form_style.input_style)
            
    #TODO override save
    
class RecycledContentEntityForm(forms.ModelForm):
    class Meta:
        model = RecycledContentEntity
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(form_style.input_style)

class EndOfLifeInformationEntityInsertForm(forms.ModelForm):
    class Meta:
        model = EndOfLifeInformationEntity
        fields = '__all__'
        
    waste_prevention = forms.FileField(widget=form_style.file_input, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    separate_collection = forms.FileField(widget=form_style.file_input, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    information_on_collection = forms.FileField(widget=form_style.file_input, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(form_style.input_style)
    
    #TODO override save

class EndOfLifeInformationEntityUpdateForm(forms.ModelForm):
    class Meta:
        model = EndOfLifeInformationEntity
        fields = '__all__'
        
    waste_prevention = forms.FileField(widget=form_style.file_input, required=False, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    separate_collection = forms.FileField(widget=form_style.file_input, required=False, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    information_on_collection = forms.FileField(widget=form_style.file_input, required=False, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(form_style.input_style)
    
    #TODO override save

class DismantlingAndRemovalDocumentationInsertForm(forms.ModelForm):
    class Meta:
        model = DismantlingAndRemovalDocumentation
        fields = '__all__'
    
    document_url = forms.FileField(widget=form_style.file_input, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(form_style.input_style)
    
    #TODO override save

class DismantlingAndRemovalDocumentationUpdateForm(forms.ModelForm):
    class Meta:
        model = DismantlingAndRemovalDocumentation
        fields = '__all__'
    
    document_url = forms.FileField(widget=form_style.file_input, required=False, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(form_style.input_style)
    
    #TODO override save

class CircularityForm(forms.ModelForm):
    class Meta:
        model = Circularity
        fields = '__all__'
        widgets = {
            'dismantling_and_removal_information': autocomplete.ModelSelect2Multiple(url='dismantling-and-removal-documentation-autocomplete', attrs=form_style.input_style),
            'spare_part_sources': autocomplete.ModelSelect2Multiple(url='spare-part-supplier-autocomplete', attrs=form_style.input_style),
            'recycled_content': autocomplete.ModelSelect2Multiple(url='recycled-content-autocomplete', attrs=form_style.input_style),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(form_style.input_style)