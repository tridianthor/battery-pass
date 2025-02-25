from django import forms

from bootstrap_datepicker_plus.widgets import DatePickerInput

import utils.form_style as form_style

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