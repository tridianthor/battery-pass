from django import forms
from django.contrib.auth.forms import SetPasswordForm, AuthenticationForm
from django.contrib.auth.hashers import make_password

from .models import Account

import utils.form_style as form_style
import utils.validators as validators

class AccountCreationForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'password', 'role']
        widgets = {
            'password': forms.PasswordInput(attrs=form_style.input_style),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(form_style.input_style)
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'role']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(form_style.input_style)
            
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
    
class ChangePasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter new password'}),
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm new password'}),
    )
    
    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("Passwords do not match. Please try again.")

        return cleaned_data
    
class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput(attrs=form_style.input_style), help_text="Email")
    password = forms.CharField(widget=forms.PasswordInput(attrs=form_style.input_style), help_text="Password")