# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models



class CarbonFootprintForBatteries(models.Model):
    battery_carbon_footprint = models.FloatField()
    carbon_footprint_per_lifecycle_stage = models.TextField()  # This field type is a guess.
    carbon_footprint_performance_class = models.TextField()
    carbon_footprint_study = models.TextField()
    absolute_carbon_footprint = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'carbon_footprint_for_batteries'


class GeneralProductInformation(models.Model):
    product_identifier = models.TextField()
    battery_passport_identifier = models.TextField()
    battery_category = models.TextField()
    manufacturer_information_contact_name = models.TextField(db_column='manufacturer_information__contact_name')  # Field renamed because it contained more than one '_' in a row.
    manufacturer_information_postal_address_address_country = models.TextField(db_column='manufacturer_information__postal_address__address_country')  # Field renamed because it contained more than one '_' in a row.
    manufacturer_information_postal_address_postal_code = models.TextField(db_column='manufacturer_information__postal_address__postal_code')  # Field renamed because it contained more than one '_' in a row.
    manufacturer_information_postal_address_street_address = models.TextField(db_column='manufacturer_information__postal_address__street_address')  # Field renamed because it contained more than one '_' in a row.
    manufacturer_information_identifier = models.TextField(db_column='manufacturer_information__identifier')  # Field renamed because it contained more than one '_' in a row.
    manufacturing_date = models.DateTimeField()
    battery_status = models.TextField()
    battery_mass = models.FloatField()
    manufacturing_place_address_country = models.TextField(db_column='manufacturing_place__address_country')  # Field renamed because it contained more than one '_' in a row.
    manufacturing_place_postal_code = models.TextField(db_column='manufacturing_place__postal_code')  # Field renamed because it contained more than one '_' in a row.
    manufacturing_place_street_address = models.TextField(db_column='manufacturing_place__street_address')  # Field renamed because it contained more than one '_' in a row.
    operator_information_contact_name = models.TextField(db_column='operator_information__contact_name')  # Field renamed because it contained more than one '_' in a row.
    operator_information_postal_address_address_country = models.TextField(db_column='operator_information__postal_address__address_country')  # Field renamed because it contained more than one '_' in a row.
    operator_information_postal_address_postal_code = models.TextField(db_column='operator_information__postal_address__postal_code')  # Field renamed because it contained more than one '_' in a row.
    operator_information_postal_address_street_address = models.TextField(db_column='operator_information__postal_address__street_address')  # Field renamed because it contained more than one '_' in a row.
    operator_information_identifier = models.TextField(db_column='operator_information__identifier')  # Field renamed because it contained more than one '_' in a row.
    putting_into_service = models.DateTimeField()
    warrenty_period = models.TextField()

    class Meta:
        managed = False
        db_table = 'general_product_information'


class Labeling(models.Model):
    declaration_of_conformity = models.TextField()
    result_of_test_report = models.TextField()
    labels = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'labeling'


class MaterialComposition(models.Model):
    battery_chemistry_short_name = models.TextField(db_column='battery_chemistry__short_name', blank=True, null=True)  # Field renamed because it contained more than one '_' in a row.
    battery_chemistry_clear_name = models.TextField(db_column='battery_chemistry__clear_name', blank=True, null=True)  # Field renamed because it contained more than one '_' in a row.
    battery_materials = models.TextField(blank=True, null=True)  # This field type is a guess.
    hazardous_substances = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'material_composition'


class PerformanceAndDurability(models.Model):
    bt_prop_original_power_capability = models.TextField()  # This field type is a guess.
    bt_prop_rated_maximum_power = models.FloatField()
    bt_prop_power_capability_ratio = models.FloatField()
    bt_prop_rated_energy = models.FloatField()
    bt_prop_expected_number_of_cycles = models.BigIntegerField()
    bt_prop_initial_self_discharge = models.FloatField()
    bt_prop_roundtrip_efficiency = models.FloatField()
    bt_prop_rated_capacity = models.FloatField()
    bt_prop_initial_internal_resistance = models.TextField()  # This field type is a guess.
    bt_prop_expected_lifetime = models.SmallIntegerField()
    bt_prop_c_rate = models.FloatField(blank=True, null=True)
    bt_prop_nominal_voltage = models.FloatField()
    bt_prop_minimum_voltage = models.FloatField()
    bt_prop_maximum_voltage = models.FloatField()
    bt_prop_capacity_threshold_for_exhaustion = models.FloatField()
    bt_prop_lifetime_reference_test = models.TextField()
    bt_prop_c_rate_life_cycle_test = models.FloatField()
    bt_prop_temperature_range_idle_state = models.FloatField()
    bc_energy_throughput = models.FloatField()
    bc_capacity_throughput_capacity_throughput_value = models.FloatField()
    bc_capacity_throughput_last_update = models.DateTimeField()
    bc_number_of_full_cycles_number_of_full_cycles_value = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    bc_number_of_full_cycles_last_update = models.DateTimeField()
    bc_state_of_certified_energy_state_of_certified_energy_value = models.FloatField()
    bc_state_of_certified_energy_last_update = models.DateTimeField()
    bc_capacity_fade_capacity_fade_value = models.FloatField()
    bc_capacity_fade_last_update = models.DateTimeField()
    bc_remaining_energy_remaining_energyalue = models.FloatField()
    bc_remaining_energy_last_update = models.DateTimeField()
    bc_remaining_capacity_remaining_capacity_value = models.FloatField()
    bc_remaining_capacity_last_update = models.DateTimeField()
    bc_negative_events = models.TextField()  # This field type is a guess.
    bc_temperature_information_time_extreme_high_temp = models.FloatField()
    bc_temperature_information_time_extreme_low_temp = models.FloatField()
    bc_temperature_information_time_extreme_high_temp_charging = models.FloatField()
    bc_temperature_information_time_extreme_low_temp_charging = models.FloatField()
    bc_temperature_information_last_update = models.DateTimeField()
    bc_remaining_power_capability = models.TextField()  # This field type is a guess.
    bc_power_fade = models.FloatField()
    bc_round_trip_efficiency_fade = models.FloatField()
    bc_evolution_of_self_discharge_evolution_of_self_discharge_enti = models.FloatField()
    bc_current_self_discharging_rate_current_self_discharging_rate_field = models.FloatField(db_column='bc_current_self_discharging_rate_current_self_discharging_rate_')  # Field renamed because it ended with '_'.
    bc_current_self_discharging_rate_last_update = models.DateTimeField()
    bc_internal_resistance_increase = models.TextField()  # This field type is a guess.
    bc_round_trip_efficiencyat50_per_cent_cycle_life = models.FloatField()
    bc_remaining_round_trip_energy_efficiency_remaining_round_trip_field = models.FloatField(db_column='bc_remaining_round_trip_energy_efficiency_remaining_round_trip_')  # Field renamed because it ended with '_'.
    bc_remaining_round_trip_energy_efficiency_last_update = models.DateTimeField()
    bc_state_of_charge_state_of_charge_value = models.FloatField()
    bc_state_of_charge_last_update = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'performance_and_durability'


class SupplyChainDueDiligence(models.Model):
    supply_chain_due_diligence_report = models.TextField()
    third_party_aussurances = models.TextField(blank=True, null=True)
    supply_chain_indicies = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'supply_chain_due_diligence'
