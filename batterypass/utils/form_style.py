from django import forms

input_style = {"class": "form-control mt-2"}

file_input = forms.FileInput(attrs=input_style) 
text_input = forms.TextInput(attrs=input_style)
text_area = forms.Textarea(attrs=input_style)
number_input = forms.NumberInput(attrs=input_style)
select = forms.Select(attrs=input_style)