from django import forms

class DueDiligenceForm(forms.Form):
    input_style = {"class": "form-control mt-2"}
    text_input = forms.FileInput(attrs=input_style) 
    
    supply_chain_due_diligence_report = forms.FileField(widget=text_input)
    third_party_assurances = forms.FileField(widget=text_input)
    supply_chain_indices = forms.FloatField(widget=forms.NumberInput(attrs=input_style))