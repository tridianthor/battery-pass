from django.contrib import admin
from dpp_admin.admin import dpp_admin
from .models import Address, ContactInformation

class AddressAdmin(admin.ModelAdmin):
    list_display = ("street_address", "postal_code", "country_name", "country_code")

    def country_name(self, obj):
        """
        Return the user-friendly name, e.g. "Germany".
        """
        return obj.country.name
    country_name.short_description = "Country Name"

    def country_code(self, obj):
        """
        Return the 2-letter ISO code, e.g. "DE".
        """
        return obj.country.code
    country_code.short_description = "ISO Code"

dpp_admin.register(Address,AddressAdmin)

class ContactInformationAdmin(admin.ModelAdmin):
    """
    Display ContactInformation, including:
    - contact_name
    - contact_role (the enum from ContactType)
    - address (linked from Address model)
    - email, phone, website if provided
    """
    list_display = ("company_name","contact_name", "role_display", "address", "email", "phone", "website")

    def role_display(self, obj):
        """
        Displays the friendly label for the contact_role enum
        (e.g. "Cell Production" instead of "cell_production").
        """
        return obj.get_contact_role_display()
    role_display.short_description = "Contact Role"

dpp_admin.register(ContactInformation,ContactInformationAdmin)