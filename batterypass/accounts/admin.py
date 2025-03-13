from django.contrib import admin
from dpp_admin.admin import dpp_admin
from .models import Account, Group
# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_active',)
    list_filter = ('is_active',)
    search_fields = ('username', 'email',)
    
dpp_admin.register(Account, AccountAdmin)

class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)
    
dpp_admin.register(Group, GroupAdmin)

