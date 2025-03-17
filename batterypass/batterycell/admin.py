# batterycell/admin.py

from django.contrib import admin
from dpp_admin.admin import dpp_admin

from .models import BatteryCell

class BatteryCellAdmin(admin.ModelAdmin):
    list_display = (
        "cell_id",
        "cell_type",
        "manufacturer_name",
        "manufacturer_country",
        "nominal_voltage",
        "rated_capacity_ah",
    )
    search_fields = ("cell_id",)
    ordering = ("-created_at",)

    def manufacturer_name(self, obj):
        """
        Pulls the manufacturer name from the related ContactInformation.
        """
        if not obj.manufacturer:
            return ""
        return obj.manufacturer.company_name

    manufacturer_name.short_description = "Manufacturer"

    def manufacturer_country(self, obj):
        """
        Pulls the manufacturer country from ContactInformation -> Address.
        """
        if not obj.manufacturer or not obj.manufacturer.address:
            return ""
        # If you're using django-countries on the address model:
        # This might show the friendly name (like "Germany").
        return obj.manufacturer.address.country.name

    manufacturer_country.short_description = "Country"
    
dpp_admin.register(BatteryCell, BatteryCellAdmin)
