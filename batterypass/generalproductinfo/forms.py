from django import forms
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.urls import reverse

from .models import GeneralProductInformation
from components.form import widget

from datetime import datetime

import utils.form as form

import traceback

class GeneralProductInfoForm(forms.ModelForm):
    class Meta:
        model = GeneralProductInformation
        exclude = ('qr_code',)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(form.input_style)