# Generated by Django 4.2.19 on 2025-03-07 02:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BatteryConditionEntity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('energy_throughput', models.FloatField()),
                ('power_fade', models.FloatField()),
                ('round_trip_efficiency_fade', models.FloatField()),
                ('round_trip_efficiency_at_50_percent_cycle_life', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='BatteryTechnicalPropertiesEntity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rated_maximum_power', models.FloatField()),
                ('power_capability_ratio', models.FloatField()),
                ('rated_energy', models.FloatField()),
                ('expected_number_of_cycles', models.BigIntegerField()),
                ('initial_self_discharge', models.FloatField()),
                ('roundtrip_efficiency', models.FloatField()),
                ('rated_capacity', models.FloatField()),
                ('expected_lifetime', models.IntegerField()),
                ('nominal_voltage', models.FloatField()),
                ('minimum_voltage', models.FloatField()),
                ('maximum_voltage', models.FloatField()),
                ('capacity_threshold_for_exhaustion', models.FloatField()),
                ('lifetime_reference_test', models.FileField(upload_to='')),
                ('c_rate_life_cycle_test', models.FloatField()),
                ('temperature_range_idle_state', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='CapacityFadeEntity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('last_update', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='CapacityThroughputEntity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('last_update', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='CurrentSelfDischargingRateEntity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('last_update', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='EvolutionOfSelfDischargeEntity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='InternalResistanceEntity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ohmic_resistance', models.FloatField()),
                ('battery_component', models.CharField(choices=[('pack', 'Pack'), ('module', 'Module'), ('cell', 'Cell')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='InternalResistanceIncreaseEntity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('last_update', models.DateTimeField()),
                ('battery_component', models.CharField(choices=[('pack', 'Pack'), ('module', 'Module'), ('cell', 'Cell')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='NegativeEventEntity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('negative_event', models.CharField(max_length=255)),
                ('last_update', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='NumberOfFullCyclesEntity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.BigIntegerField()),
                ('last_update', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='PowerCapabilityAtEntity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('at_soc', models.FloatField()),
                ('power_capability_at', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='RemainingCapacityEntity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('last_update', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='RemainingEnergyEntity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('last_update', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='RemainingPowerCapabilityEntity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('last_update', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='RemainingRoundTripEnergyEfficiencyEntity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('last_update', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='StateOfCertifiedEnergyEntity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('last_update', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='StateOfChargeEntity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('last_update', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='TemperatureConditionsEntity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_extreme_high_temp', models.FloatField()),
                ('time_extreme_low_temp', models.FloatField()),
                ('time_extreme_high_temp_charging', models.FloatField()),
                ('time_extreme_low_temp_charging', models.FloatField()),
                ('last_update', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='PerformanceAndDurability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('battery_condition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='performance.batteryconditionentity')),
                ('battery_technical_properties', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='performance.batterytechnicalpropertiesentity')),
            ],
        ),
        migrations.AddField(
            model_name='batteryconditionentity',
            name='capacity_fade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='performance.capacityfadeentity'),
        ),
        migrations.AddField(
            model_name='batteryconditionentity',
            name='capacity_throughput',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='performance.capacitythroughputentity'),
        ),
        migrations.AddField(
            model_name='batteryconditionentity',
            name='current_self_discharging_rate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='performance.currentselfdischargingrateentity'),
        ),
        migrations.AddField(
            model_name='batteryconditionentity',
            name='evolution_of_self_discharge',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='performance.evolutionofselfdischargeentity'),
        ),
        migrations.AddField(
            model_name='batteryconditionentity',
            name='number_of_full_cycles',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='performance.numberoffullcyclesentity'),
        ),
        migrations.AddField(
            model_name='batteryconditionentity',
            name='remaining_capacity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='performance.remainingcapacityentity'),
        ),
        migrations.AddField(
            model_name='batteryconditionentity',
            name='remaining_energy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='performance.remainingenergyentity'),
        ),
        migrations.AddField(
            model_name='batteryconditionentity',
            name='remaining_round_trip_energy_efficiency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='performance.remainingroundtripenergyefficiencyentity'),
        ),
        migrations.AddField(
            model_name='batteryconditionentity',
            name='state_of_certified_energy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='performance.stateofcertifiedenergyentity'),
        ),
        migrations.AddField(
            model_name='batteryconditionentity',
            name='state_of_charge',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='performance.stateofchargeentity'),
        ),
        migrations.AddField(
            model_name='batteryconditionentity',
            name='temperature_information',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='performance.temperatureconditionsentity'),
        ),
    ]
