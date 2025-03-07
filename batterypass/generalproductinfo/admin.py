from django.contrib import admin
from .models import PostalAddressEntity, ContactInformationEntity, GeneralProductInformation

# Register your models here.

admin.site.register(PostalAddressEntity)
admin.site.register(ContactInformationEntity)
admin.site.register(GeneralProductInformation)