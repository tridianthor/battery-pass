from django.contrib import admin
from dpp_admin.admin import dpp_admin
from .models import PostalAddressEntity, ContactInformationEntity, GeneralProductInformation

# Register your models here.

dpp_admin.register(PostalAddressEntity)
dpp_admin.register(ContactInformationEntity)
dpp_admin.register(GeneralProductInformation)