from django import forms

class DueDiligenceForm(forms.Form):
    supply_chain_due_diligence_report = forms.URLField()
    third_party_assurances = forms.URLField()
    supply_chain_indices = forms.FloatField()