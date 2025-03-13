from django.contrib import admin
from dpp_admin.admin import dpp_admin
from .models import BatteryLocationEntity, BatteryMaterialEntity, HazardousSubstanceEntity
from .models import BatteryChemistryEntity, MaterialComposition
# Register your models here.

class BatteryLocationEntityAdmin(admin.ModelAdmin):
    list_display = ('component_name', 'component_id')
    search_fields = ('component_name', 'component_id')

dpp_admin.register(BatteryLocationEntity, BatteryLocationEntityAdmin)

class BatteryMaterialEntityAdmin(admin.ModelAdmin):
    list_display = ('battery_material_name', 'battery_material_identifier', 'battery_material_mass')
    search_fields = ('battery_material_name', 'battery_material_identifier')

dpp_admin.register(BatteryMaterialEntity, BatteryMaterialEntityAdmin)

class HazardousSubstanceEntityAdmin(admin.ModelAdmin):
    list_display = ('hazardous_substance_name', 'hazardous_substance_identifier', 'hazardous_substance_concentration')
    search_fields = ('hazardous_substance_name', 'hazardous_substance_identifier')

dpp_admin.register(HazardousSubstanceEntity, HazardousSubstanceEntityAdmin)

class BatteryChemistryEntityAdmin(admin.ModelAdmin):
    list_display = ('clear_name', 'short_name')
    search_fields = ('clear_name', 'short_name')

dpp_admin.register(BatteryChemistryEntity, BatteryChemistryEntityAdmin)

class MaterialCompositionAdmin(admin.ModelAdmin):
    list_display = ('clear_name', 'short_name',)
    search_fields = ('clear_name', 'short_name')
    
    def clear_name(self, obj):
        return obj.battery_chemistry.short_name
    
    def short_name(self, obj):
        return obj.battery_chemistry.clear_name

dpp_admin.register(MaterialComposition, MaterialCompositionAdmin)