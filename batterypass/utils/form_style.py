from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput

input_style = {"class": "form-control"}
date_input_style = {"class": "form-control"}

file_input = forms.FileInput(attrs=input_style) 
text_input = forms.TextInput(attrs=input_style)
text_area = forms.Textarea(attrs=input_style)
number_input = forms.NumberInput(attrs=input_style)
select = forms.Select(attrs=input_style)
date_input = DatePickerInput(options={'locale': 'en', 'format': 'DD/MM/YYYY'}, attrs=date_input_style)