from django.contrib import admin
import performance.models as models
# Register your models here.

admin.site.register(models.InternalResistanceEntity)
admin.site.register(models.EvolutionOfSelfDischargeEntity)
admin.site.register(models.CapacityFadeEntity)
admin.site.register(models.CapacityThroughputEntity)
admin.site.register(models.InternalResistanceIncreaseEntity)
admin.site.register(models.NumberOfFullCyclesEntity)
admin.site.register(models.RemainingCapacityEntity)
admin.site.register(models.RemainingEnergyEntity)
admin.site.register(models.RemainingRoundTripEnergyEfficiencyEntity)
admin.site.register(models.RemainingPowerCapabilityEntity)
admin.site.register(models.StateOfChargeEntity)
admin.site.register(models.StateOfCertifiedEnergyEntity)
admin.site.register(models.CurrentSelfDischargingRateEntity)
admin.site.register(models.TemperatureConditionsEntity)
admin.site.register(models.PowerCapabilityAtEntity)
admin.site.register(models.BatteryTechnicalPropertiesEntity)
admin.site.register(models.BatteryConditionEntity)
admin.site.register(models.PerformanceAndDurability)
