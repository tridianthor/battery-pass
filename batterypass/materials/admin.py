from django.contrib import admin
from dpp_admin.admin import dpp_admin
from .models import (
    BatteryLocationEntity,
    BatteryMaterialEntity,
    HazardousSubstanceEntity,
    BatteryChemistryEntity,
    MaterialComposition,
    ESGPerformance,
)

class BatteryLocationAdmin(admin.ModelAdmin):
    list_display = ("component_name", "component_id", "created_at")
    search_fields = ("component_name", "component_id")
    ordering = ("created_at",)
dpp_admin.register(BatteryLocationEntity,BatteryLocationAdmin)

class BatteryMaterialAdmin(admin.ModelAdmin):
    list_display = ("battery_material_name", "battery_material_identifier", "battery_material_mass", "is_critical_raw_material", "created_at")
    search_fields = ("battery_material_name", "battery_material_identifier")
    list_filter = ("is_critical_raw_material",)
    ordering = ("created_at",)
dpp_admin.register(BatteryMaterialEntity,BatteryMaterialAdmin)

class HazardousSubstanceAdmin(admin.ModelAdmin):
    list_display = ("hazardous_substance_name", "hazardous_substance_identifier", "hazardous_substance_class", "hazardous_substance_concentration", "created_at")
    search_fields = ("hazardous_substance_name", "hazardous_substance_identifier")
    list_filter = ("hazardous_substance_class",)
    ordering = ("created_at",)
dpp_admin.register(HazardousSubstanceEntity, HazardousSubstanceAdmin)

class BatteryChemistryAdmin(admin.ModelAdmin):
    list_display = ("clear_name", "short_name", "created_at")
    search_fields = ("clear_name", "short_name")
    ordering = ("created_at",)
dpp_admin.register(BatteryChemistryEntity,BatteryChemistryAdmin)

class ESGPerformanceAdmin(admin.ModelAdmin):
    list_display = (
        "id_short", "carbon_footprint", "renewable_energy_use", "water_consumption", 
        "social_impact", "worker_safety_standards", "governance_compliance", "recycling_efficiency", "created_at"
    )
    search_fields = ("carbon_footprint", "social_impact", "governance_compliance")
    list_filter = ("carbon_footprint", "worker_safety_standards", "governance_compliance")
    ordering = ("created_at",)
dpp_admin.register(ESGPerformance, ESGPerformanceAdmin)

class MaterialCompositionAdmin(admin.ModelAdmin):
    list_display = (
        "material_composition_id", "battery_chemistry", "traceability", 
        "tracing_period_start", "tracing_period_end", "physical_amount", 
        "traced_amount","esg_performance_summary", "esg_performance", "version", "created_at"
    )
    
    list_filter = ("battery_chemistry", "traceability","esg_performance_summary")  
    search_fields = ("material_composition_id", "battery_chemistry__clear_name")  
    ordering = ("created_at",)  

    fieldsets = (
        ("Basic Information", {
            "fields": ("material_composition_id", "battery_chemistry", "version", "created_at")
        }),
        ("Traceability", {
            "fields": ("traceability", "tracing_period_start", "tracing_period_end")
        }),
        ("Material Details", {
            "fields": ("first_traced_material", "second_traced_material", "physical_amount", "traced_amount")
        }),
        ("Location & Compliance", {
            "fields": ("manufacturer", "esg_performance", "esg_performance_summary")
        }),
        ("Technical Information", {
            "fields": ("hash_signature",)
        }),
    )
    readonly_fields = ("created_at",)  # Mark `created_at` as read-only

    # Show country name in Admin
    def get_country(self, obj):
        return obj.country.country_name if obj.country else "N/A"
    get_country.short_description = "Country"

    # Show country code in Admin
    def get_country_code(self, obj):
        return obj.country.country_code if obj.country else "N/A"
    get_country_code.short_description = "Country Code"

    # Show ESG Performance Summary Choice Label
    def esg_performance_summary_display(self, obj):
        return obj.get_esg_performance_summary_display() if obj.esg_performance_summary else "N/A"
    esg_performance_summary_display.short_description = "ESG Summary"

dpp_admin.register(MaterialComposition,MaterialCompositionAdmin)