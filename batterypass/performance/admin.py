from django.contrib import admin
from dpp_admin.admin import dpp_admin
import performance.models as models
# Register your models here.

dpp_admin.register(models.InternalResistanceEntity)
dpp_admin.register(models.EvolutionOfSelfDischargeEntity)
dpp_admin.register(models.CapacityFadeEntity)
dpp_admin.register(models.CapacityThroughputEntity)
dpp_admin.register(models.InternalResistanceIncreaseEntity)
dpp_admin.register(models.NumberOfFullCyclesEntity)
dpp_admin.register(models.RemainingCapacityEntity)
dpp_admin.register(models.RemainingEnergyEntity)
dpp_admin.register(models.RemainingRoundTripEnergyEfficiencyEntity)
dpp_admin.register(models.RemainingPowerCapabilityEntity)
dpp_admin.register(models.StateOfChargeEntity)
dpp_admin.register(models.StateOfCertifiedEnergyEntity)
dpp_admin.register(models.CurrentSelfDischargingRateEntity)
dpp_admin.register(models.TemperatureConditionsEntity)
dpp_admin.register(models.PowerCapabilityAtEntity)

class BatteryTechnicalPropertiesEntityAdmin(admin.ModelAdmin):
    list_display = ('rated_maximum_power', 'power_capability_ratio', 'rated_energy', 'expected_number_of_cycles',)
    list_filter = ('rated_maximum_power', 'power_capability_ratio', 'rated_energy', 'expected_number_of_cycles',)
    search_fields = ('rated_maximum_power', 'power_capability_ratio', 'rated_energy', 'expected_number_of_cycles',)

dpp_admin.register(models.BatteryTechnicalPropertiesEntity, BatteryTechnicalPropertiesEntityAdmin)

class BatteryConditionEntityAdmin(admin.ModelAdmin):
    list_display = ('energy_throughput', 'power_fade', 'round_trip_efficiency_fade', 'round_trip_efficiency_at_50_percent_cycle_life',)
    list_filter = ('energy_throughput', 'power_fade', 'round_trip_efficiency_fade', 'round_trip_efficiency_at_50_percent_cycle_life',)
    search_fields = ('energy_throughput', 'power_fade', 'round_trip_efficiency_fade', 'round_trip_efficiency_at_50_percent_cycle_life',)

dpp_admin.register(models.BatteryConditionEntity, BatteryConditionEntityAdmin)
dpp_admin.register(models.PerformanceAndDurability)
