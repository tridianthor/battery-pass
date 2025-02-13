# Generated by Django 5.1.5 on 2025-02-12 09:30

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ComponentEntity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_name', models.CharField(max_length=255)),
                ('part_number', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DismantlingAndRemovalDocumentation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_type', models.CharField(choices=[('BillOfMaterial', 'Bill of Material'), ('Model3D', 'Model 3D'), ('DismantlingManual', 'Dismantling Manual'), ('RemovalManual', 'Removal Manual'), ('OtherManual', 'Other Manual'), ('Drawing', 'Drawing')], max_length=50)),
                ('mime_type', models.CharField(max_length=50)),
                ('document_url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='EndOfLifeInformationEntity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('waste_prevention', models.URLField()),
                ('separate_collection', models.URLField()),
                ('information_on_collection', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='PostalAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=100)),
                ('postal_code', models.CharField(max_length=20)),
                ('street_address', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='RecycledContentEntity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pre_consumer_share', models.FloatField()),
                ('recycled_material', models.CharField(choices=[('Cobalt', 'Cobalt'), ('Nickel', 'Nickel'), ('Lithium', 'Lithium'), ('Lead', 'Lead')], max_length=50)),
                ('post_consumer_share', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='SafetyMeasuresEntity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('safety_instructions', models.URLField()),
                ('extinguishing_agent', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='SparePartSupplierEntity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_of_supplier', models.CharField(max_length=255)),
                ('email_address_of_supplier', models.EmailField(max_length=254)),
                ('supplier_web_address', models.URLField()),
                ('address_of_supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='circularity.postaladdress')),
                ('components', models.ManyToManyField(related_name='suppliers', to='circularity.componententity')),
            ],
        ),
        migrations.CreateModel(
            name='Circularity',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('renewable_content', models.FloatField()),
                ('dismantling_and_removal_information', models.ManyToManyField(related_name='circularities', to='circularity.dismantlingandremovaldocumentation')),
                ('end_of_life_information', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='circularity.endoflifeinformationentity')),
                ('recycled_content', models.ManyToManyField(related_name='circularities', to='circularity.recycledcontententity')),
                ('safety_measures', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='circularity.safetymeasuresentity')),
                ('spare_part_sources', models.ManyToManyField(related_name='circularities', to='circularity.sparepartsupplierentity')),
            ],
        ),
    ]
