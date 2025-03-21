from django.contrib import admin
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse

from .forms import BootstrapAuthenticationForm

class DPPAdmin(admin.AdminSite):
    site_header = 'DPP Administration'
    site_title = 'DPP Admin'
    index_title = 'Welcome to DPP Admin'
    
    def login(self, request, extra_context=None):
        if request.method == 'POST':
            forms = BootstrapAuthenticationForm(request, data=request.POST)
            if forms.is_valid():
                username = forms.cleaned_data.get('username')
                password = forms.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect(reverse('admin:index'))
                else:
                    forms.add_error(None, "Invalid username or password.")
        else:
            forms = BootstrapAuthenticationForm(request)

        context = {
            **self.each_context(request),
            'title': 'Log in',
            'app_path': request.get_full_path(),
            'forms': forms,
        }
        return render(request, 'admin/login.html', context)
    
dpp_admin = DPPAdmin()