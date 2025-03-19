from django.contrib import admin
from dpp_admin.admin import dpp_admin
from .models import PostalAddressEntity, GeneralProductInformation

# Register your models here.

dpp_admin.register(PostalAddressEntity)

class GeneralProductInformationAdmin(admin.ModelAdmin):
    exclude = ('qr_code',)

dpp_admin.register(GeneralProductInformation, GeneralProductInformationAdmin)