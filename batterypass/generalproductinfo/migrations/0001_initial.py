# Generated by Django 5.1.5 on 2025-02-12 09:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactInformationEntity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_name', models.CharField(max_length=255)),
                ('identifier', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PostalAddressEntity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_country', models.CharField(max_length=100)),
                ('postal_code', models.CharField(max_length=20)),
                ('street_address', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='GeneralProductInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_identifier', models.CharField(max_length=255, unique=True)),
                ('battery_passport_identifier', models.CharField(max_length=255, unique=True)),
                ('battery_category', models.CharField(choices=[('lmt', 'LMT'), ('ev', 'EV'), ('industrial', 'Industrial'), ('stationary', 'Stationary')], max_length=50)),
                ('manufacturing_date', models.DateField()),
                ('battery_status', models.CharField(choices=[('Original', 'Original'), ('Repurposed', 'Repurposed'), ('Reused', 'Reused'), ('Remanufactured', 'Remanufactured'), ('Waste', 'Waste')], max_length=50)),
                ('battery_mass', models.FloatField()),
                ('putting_into_service', models.DateField()),
                ('warranty_period', models.DateField()),
                ('manufacturer_information', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manufacturers', to='generalproductinfo.contactinformationentity')),
                ('operator_information', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operators', to='generalproductinfo.contactinformationentity')),
                ('manufacturing_place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manufacturing_places', to='generalproductinfo.postaladdressentity')),
            ],
        ),
        migrations.AddField(
            model_name='contactinformationentity',
            name='postal_address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generalproductinfo.postaladdressentity'),
        ),
    ]
