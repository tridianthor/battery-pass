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

def split_form(form):
    fields = list(form)
    fields_per_column = 5
    field_rows = []

    for i in range(0, len(fields), fields_per_column * 2):
        left_fields = fields[i:i + fields_per_column]
        right_fields = fields[i + fields_per_column:i + fields_per_column * 2]
        field_rows.append({
            'left_fields': left_fields,
            'right_fields': right_fields,
        })
    
    return field_rows