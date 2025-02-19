from django import forms
from django.core.validators import FileExtensionValidator
from django.contrib import admin
from django.contrib.admin.widgets import AutocompleteSelect

from .models import Labeling, LabelingEntity, LabelingSubject

from dal import autocomplete

import utils.form_style as form_style
import utils.validators as validators

class LabelingForm(forms.ModelForm):
    class Meta:
        model = Labeling
        fields = '__all__'
        widgets = {
            'labels': autocomplete.ModelSelect2Multiple(url='labels-autocomplete', attrs=form_style.input_style)
        }

    declaration_of_conformity = forms.FileField(widget=form_style.file_input, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    result_of_test_report = forms.FileField(widget=form_style.file_input, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])

class LabelsRelationForm(forms.ModelForm):
    class Meta:
        model = Labeling
        fields = ['labels']
        widgets = {
            'labels': autocomplete.ModelSelect2Multiple(url='labels-autocomplete', attrs=form_style.input_style)
        }

class LabelingEntityForm(forms.ModelForm):
    class Meta:
        model = LabelingEntity
        fields = '__all__'
        widgets = {
            'labeling_subject': form_style.select
        }
        
    labeling_symbol = forms.FileField(widget=form_style.file_input, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    labeling_meaning = forms.JSONField(widget=form_style.text_area, validators=[validators.validate_json])
    
    