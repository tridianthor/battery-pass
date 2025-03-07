# Generated by Django 4.2.19 on 2025-03-07 02:24

import django.core.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SupplyChainDueDiligence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_short', models.CharField(default=uuid.uuid4, max_length=255, unique=True)),
                ('semantic_id', models.URLField(blank=True, null=True)),
                ('supply_chain_id', models.CharField(max_length=255, unique=True)),
                ('supply_chain_due_diligence_report', models.FileField(max_length=255, upload_to='')),
                ('third_party_assurances', models.FileField(blank=True, null=True, upload_to='')),
                ('supply_chain_indices', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('hash_signature', models.CharField(blank=True, max_length=256, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('version', models.IntegerField(default=1)),
            ],
        ),
    ]
