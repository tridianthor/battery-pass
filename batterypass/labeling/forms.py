from django import forms
from django.core.validators import FileExtensionValidator
from django.contrib import admin
from django.contrib.admin.widgets import AutocompleteSelect

from .models import Labeling, LabelingEntity, LabelingSubject
from .const import declaration_path, result_of_test_path, labeling_symbol_path
from dal import autocomplete

from datetime import datetime

import utils.form as form
import utils.validators as validators
from utils.upload_util import Upload

import traceback
class LabelingInsertForm(forms.ModelForm):
    class Meta:
        model = Labeling
        fields = '__all__'
        widgets = {
            'labels': autocomplete.ModelSelect2Multiple(url='labels_autocomplete', attrs=form.input_style)
        }

    declaration_of_conformity = forms.FileField(widget=form.file_input, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    result_of_test_report = forms.FileField(widget=form.file_input, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(form.input_style)
class LabelingUpdateForm(forms.ModelForm):
    class Meta:
        model = Labeling
        fields = '__all__'
        widgets = {
            'labels': autocomplete.ModelSelect2Multiple(url='labels_autocomplete', attrs=form.input_style)
        }
    
    declaration_of_conformity = forms.FileField(widget=form.file_input, required=False, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    result_of_test_report = forms.FileField(widget=form.file_input, required=False, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(form.input_style)

class LabelingEntityInsertForm(forms.ModelForm):
    class Meta:
        model = LabelingEntity
        fields = '__all__'
        widgets = {
            'labeling_subject': form.select
        }
        
    labeling_symbol = forms.FileField(widget=form.file_input, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    labeling_meaning = forms.JSONField(widget=form.text_area, validators=[validators.validate_json])
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(form.input_style)
class LabelingEntityUpdateForm(forms.ModelForm):
    class Meta:
        model = LabelingEntity
        fields = '__all__'
        widgets = {
            'labeling_subject': form.select
        }
        
    labeling_symbol = forms.FileField(widget=form.file_input, required=False, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    labeling_meaning = forms.JSONField(widget=form.text_area, required=False, validators=[validators.validate_json])
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(form.input_style)