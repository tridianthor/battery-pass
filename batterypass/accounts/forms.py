from django import forms
from django.contrib.auth.forms import SetPasswordForm, AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, Permission

from .models import Account

from dal import autocomplete

import utils.form_style as form_style
import utils.validators as validators

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'permissions']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'permissions': autocomplete.ModelSelect2Multiple(url='permission-autocomplete', attrs=form_style.input_style),
        }
        
    check_all = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False, initial=False)
        
    def clean_name(self):
        name = self.cleaned_data['name']
        if self.instance.pk:
            return name
        if Group.objects.filter(name=name).exists():
            raise forms.ValidationError('A group with this name already exists.')
        return name

class AccountInsertForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'password', 'groups']
        widgets = {
            'password': forms.PasswordInput(attrs=form_style.input_style),
        }
    
    groups = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        label="Group",
        widget=forms.Select,
        required=True
    )

        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['groups'].initial = self.instance.groups.all()
        for field_name, field in self.fields.items():
            field.widget.attrs.update(form_style.input_style)
        
    def clean_password(self):
        password = self.cleaned_data.get('password')
        #validators.validate_password_complexity(password)
        return password
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
            user.groups.clear()
            user.groups.add(self.cleaned_data['groups'])
        return user
    
class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'groups']
    
    groups = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        label="Group",
        widget=forms.Select,
        required=True
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.groups.exists():
            self.fields['groups'].initial = self.instance.groups.first()
        for field_name, field in self.fields.items():
            field.widget.attrs.update(form_style.input_style)

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user.groups.clear()
            user.groups.add(self.cleaned_data['groups'])
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