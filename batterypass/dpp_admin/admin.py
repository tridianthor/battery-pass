from django.contrib import admin

class DPPAdmin(admin.AdminSite):
    site_header = 'DPP Administration'
    site_title = 'DPP Admin'
    index_title = 'Welcome to DPP Admin'
    
dpp_admin = DPPAdmin()