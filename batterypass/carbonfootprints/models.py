from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
import uuid



class LifecycleStage(models.TextChoices):
    RAW_MATERIAL_EXTRACTION = "RawMaterialExtraction", "Raw Material Extraction"
    MAIN_PRODUCTION = "MainProduction", "Main Production"
    DISTRIBUTION = "Distribution", "Distribution"
    RECYCLING = "Recycling", "Recycling"


class CarbonFootprintPerLifecycleStageEntity(models.Model):
    id_short = models.CharField(max_length=255, unique=True, default=uuid.uuid4)  # AAS-compatible identifier
    semantic_id = models.URLField(blank=True, null=True)  # Standardized reference

    lifecycle_stage = models.CharField(
        max_length=50, choices=LifecycleStage.choices
    )
    carbon_footprint = models.FloatField(validators=[MinValueValidator(0)])  # Ensures non-negative values

    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for data creation
    version = models.IntegerField(default=1)  # Versioning for tracking changes

    def __str__(self):
        return f"{self.lifecycle_stage} - {self.carbon_footprint} kgCO2"


class CarbonFootprintForBatteries(models.Model):
    id_short = models.CharField(max_length=255, unique=True, default=uuid.uuid4)  # AAS-compatible identifier
    semantic_id = models.URLField(blank=True, null=True)  # Standardized reference

    battery_id = models.CharField(max_length=255, unique=True)  # Standardized battery identifier
    battery_carbon_footprint = models.FloatField(validators=[MinValueValidator(0)])  # Ensures no negative footprint
    carbon_footprint_per_lifecycle_stage = models.ManyToManyField(
        CarbonFootprintPerLifecycleStageEntity, related_name="batteries"
    )
    carbon_footprint_performance_class = models.CharField(max_length=255)
    carbon_footprint_study = models.FileField()

    absolute_carbon_footprint = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])

    hash_signature = models.CharField(max_length=256, null=True, blank=True)  # Blockchain readiness

    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp
    version = models.IntegerField(default=1)  # Versioning

    def __str__(self):
        return f"Battery Carbon Footprint: {self.battery_carbon_footprint} kgCO2"
