from django.db import models

import uuid
# Create your models here.

class BatteryComponent(models.TextChoices):
    PACK = "pack", "Pack"
    MODULE = "module", "Module"
    CELL = "cell", "Cell"


class InternalResistanceEntity(models.Model):
    ohmic_resistance = models.FloatField()
    battery_component = models.CharField(
        max_length=20, choices=BatteryComponent.choices
    )

    def __str__(self):
        return f"Internal Resistance: {self.ohmic_resistance} Ω - {self.battery_component}"


class EvolutionOfSelfDischargeEntity(models.Model):
    value = models.FloatField()

    def __str__(self):
        return f"Self-Discharge Evolution: {self.value}%"


class CapacityFadeEntity(models.Model):
    value = models.FloatField()
    last_update = models.DateTimeField()

    def __str__(self):
        return f"Capacity Fade: {self.value}% (Last Updated: {self.last_update})"


class CapacityThroughputEntity(models.Model):
    value = models.FloatField()
    last_update = models.DateTimeField()

    def __str__(self):
        return f"Capacity Throughput: {self.value} Ah (Last Updated: {self.last_update})"


class InternalResistanceIncreaseEntity(models.Model):
    value = models.FloatField()
    last_update = models.DateTimeField()
    battery_component = models.CharField(
        max_length=20, choices=BatteryComponent.choices
    )

    def __str__(self):
        return f"Resistance Increase: {self.value} Ω ({self.battery_component})"


class NumberOfFullCyclesEntity(models.Model):
    value = models.BigIntegerField()
    last_update = models.DateTimeField()

    def __str__(self):
        return f"Full Cycles: {self.value} (Last Updated: {self.last_update})"


class RemainingCapacityEntity(models.Model):
    value = models.FloatField()
    last_update = models.DateTimeField()

    def __str__(self):
        return f"Remaining Capacity: {self.value}% (Last Updated: {self.last_update})"


class RemainingEnergyEntity(models.Model):
    value = models.FloatField()
    last_update = models.DateTimeField()

    def __str__(self):
        return f"Remaining Energy: {self.value} kWh (Last Updated: {self.last_update})"


class RemainingRoundTripEnergyEfficiencyEntity(models.Model):
    value = models.FloatField()
    last_update = models.DateTimeField()

    def __str__(self):
        return f"Round Trip Efficiency: {self.value}% (Last Updated: {self.last_update})"


class RemainingPowerCapabilityEntity(models.Model):
    value = models.FloatField()
    last_update = models.DateTimeField()

    def __str__(self):
        return f"Power Capability: {self.value} kW (Last Updated: {self.last_update})"


class StateOfChargeEntity(models.Model):
    value = models.FloatField()
    last_update = models.DateTimeField()

    def __str__(self):
        return f"State of Charge: {self.value}% (Last Updated: {self.last_update})"


class StateOfCertifiedEnergyEntity(models.Model):
    value = models.FloatField()
    last_update = models.DateTimeField()

    def __str__(self):
        return f"Certified Energy State: {self.value} kWh (Last Updated: {self.last_update})"


class CurrentSelfDischargingRateEntity(models.Model):
    value = models.FloatField()
    last_update = models.DateTimeField()

    def __str__(self):
        return f"Self-Discharge Rate: {self.value}%/day (Last Updated: {self.last_update})"


class TemperatureConditionsEntity(models.Model):
    time_extreme_high_temp = models.FloatField()
    time_extreme_low_temp = models.FloatField()
    time_extreme_high_temp_charging = models.FloatField()
    time_extreme_low_temp_charging = models.FloatField()
    last_update = models.DateTimeField()

    def __str__(self):
        return f"Temperature Extremes (Updated: {self.last_update})"


class PowerCapabilityAtEntity(models.Model):
    at_soc = models.FloatField()
    power_capability_at = models.FloatField()

    def __str__(self):
        return f"Power Capability at {self.at_soc}% SoC: {self.power_capability_at} kW"


class BatteryTechnicalPropertiesEntity(models.Model):
    rated_maximum_power = models.FloatField()
    power_capability_ratio = models.FloatField()
    rated_energy = models.FloatField()
    expected_number_of_cycles = models.BigIntegerField()
    initial_self_discharge = models.FloatField()
    roundtrip_efficiency = models.FloatField()
    rated_capacity = models.FloatField()
    expected_lifetime = models.IntegerField()
    nominal_voltage = models.FloatField()
    minimum_voltage = models.FloatField()
    maximum_voltage = models.FloatField()
    capacity_threshold_for_exhaustion = models.FloatField()
    lifetime_reference_test = models.URLField()
    c_rate_life_cycle_test = models.FloatField()
    temperature_range_idle_state = models.FloatField()

    def __str__(self):
        return f"Battery Technical Properties - Rated Power: {self.rated_maximum_power} kW"


class BatteryConditionEntity(models.Model):
    energy_throughput = models.FloatField()
    capacity_throughput = models.ForeignKey(CapacityThroughputEntity, on_delete=models.CASCADE)
    number_of_full_cycles = models.ForeignKey(NumberOfFullCyclesEntity, on_delete=models.CASCADE)
    state_of_certified_energy = models.ForeignKey(StateOfCertifiedEnergyEntity, on_delete=models.CASCADE)
    capacity_fade = models.ForeignKey(CapacityFadeEntity, on_delete=models.CASCADE)
    remaining_energy = models.ForeignKey(RemainingEnergyEntity, on_delete=models.CASCADE)
    remaining_capacity = models.ForeignKey(RemainingCapacityEntity, on_delete=models.CASCADE)
    temperature_information = models.ForeignKey(TemperatureConditionsEntity, on_delete=models.CASCADE)
    power_fade = models.FloatField()
    round_trip_efficiency_fade = models.FloatField()
    evolution_of_self_discharge = models.ForeignKey(EvolutionOfSelfDischargeEntity, on_delete=models.CASCADE)
    current_self_discharging_rate = models.ForeignKey(CurrentSelfDischargingRateEntity, on_delete=models.CASCADE)
    round_trip_efficiency_at_50_percent_cycle_life = models.FloatField()
    remaining_round_trip_energy_efficiency = models.ForeignKey(
        RemainingRoundTripEnergyEfficiencyEntity, on_delete=models.CASCADE
    )
    state_of_charge = models.ForeignKey(StateOfChargeEntity, on_delete=models.CASCADE)

    def __str__(self):
        return f"Battery Condition - Energy Throughput: {self.energy_throughput} kWh"


class PerformanceAndDurability(models.Model):
    id = models.BigAutoField(primary_key=True)
    battery_technical_properties = models.ForeignKey(BatteryTechnicalPropertiesEntity, on_delete=models.CASCADE)
    battery_condition = models.ForeignKey(BatteryConditionEntity, on_delete=models.CASCADE)

    def __str__(self):
        return f"Performance and Durability Data"

class NegativeEventEntity(models.Model):
    negative_event = models.CharField(max_length=255)
    last_update = models.DateTimeField()

    def __str__(self):
        return f"Negative Event: {self.negative_event} (Last Updated: {self.last_update})"