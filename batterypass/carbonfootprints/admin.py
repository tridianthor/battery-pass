from django.contrib import admin
from dpp_admin.admin import dpp_admin
from .models import CarbonFootprintForBatteries, CarbonFootprintPerLifecycleStageEntity

class CarbonFootprintForBatteriesAdmin(admin.ModelAdmin):
    list_display = ('id_short', 'battery_id', 'battery_carbon_footprint', 'carbon_footprint_performance_class', 'created_at', 'version')
    search_fields = ('battery_id', 'carbon_footprint_performance_class')
    list_filter = ('carbon_footprint_performance_class', 'created_at')

dpp_admin.register(CarbonFootprintForBatteries, CarbonFootprintForBatteriesAdmin)

class CarbonFootprintPerLifecycleStageEntityAdmin(admin.ModelAdmin):
    list_display = ('id_short', 'lifecycle_stage', 'carbon_footprint', 'created_at', 'version')
    search_fields = ('lifecycle_stage', 'carbon_footprint')
    list_filter = ('lifecycle_stage', 'created_at')

dpp_admin.register(CarbonFootprintPerLifecycleStageEntity, CarbonFootprintPerLifecycleStageEntityAdmin)
