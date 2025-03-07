from django.db import models
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator


class HazardousSubstanceClassCharacteristic(models.TextChoices):
    ACUTE_TOXICITY = "AcuteToxicity", "Acute Toxicity"
    SKIN_CORROSION_OR_IRRITATION = "SkinCorrosionOrIrritation", "Skin Corrosion or Irritation"
    EYE_DAMAGE_OR_IRRITATION = "EyeDamageOrIrritation", "Eye Damage or Irritation"


class BatteryLocationEntity(models.Model):
    id_short = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    semantic_id = models.URLField(blank=True, null=True)

    component_name = models.CharField(max_length=255)
    component_id = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    version = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.component_name} ({self.component_id})" if self.component_id else self.component_name


class BatteryMaterialEntity(models.Model):
    id_short = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    semantic_id = models.URLField(blank=True, null=True)

    battery_material_location = models.ForeignKey(BatteryLocationEntity, on_delete=models.CASCADE)
    battery_material_identifier = models.CharField(max_length=50, unique=True)  # Standardized identifier
    battery_material_name = models.CharField(max_length=255)
    battery_material_mass = models.FloatField(validators=[MinValueValidator(0)])  # Ensures no negative mass
    is_critical_raw_material = models.BooleanField()

    created_at = models.DateTimeField(auto_now_add=True)
    version = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.battery_material_name} ({self.battery_material_identifier})"


class HazardousSubstanceEntity(models.Model):
    id_short = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    semantic_id = models.URLField(blank=True, null=True)

    hazardous_substance_class = models.CharField(
        max_length=50, choices=HazardousSubstanceClassCharacteristic.choices
    )
    hazardous_substance_name = models.CharField(max_length=255)
    hazardous_substance_concentration = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )  # Ensuring valid concentration %
    hazardous_substance_impact = models.JSONField()  # Stores impacts as JSON
    hazardous_substance_location = models.ForeignKey(BatteryLocationEntity, on_delete=models.CASCADE)
    hazardous_substance_identifier = models.CharField(max_length=50, unique=True)  # Standardized identifier

    created_at = models.DateTimeField(auto_now_add=True)
    version = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.hazardous_substance_name} ({self.hazardous_substance_identifier})"


class BatteryChemistryEntity(models.Model):
    id_short = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    semantic_id = models.URLField(blank=True, null=True)

    short_name = models.CharField(max_length=100, unique=True)
    clear_name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    version = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.clear_name} ({self.short_name})"


class MaterialComposition(models.Model):
    id_short = models.CharField(max_length=255, unique=True, default=uuid.uuid4)  # AAS-compatible ID
    semantic_id = models.URLField(blank=True, null=True)  # Standardized reference

    material_composition_id = models.CharField(max_length=255, unique=True)  # Standardized identifier
    battery_chemistry = models.ForeignKey(BatteryChemistryEntity, on_delete=models.CASCADE)
    battery_materials = models.ManyToManyField(BatteryMaterialEntity, related_name="materials")
    hazardous_substances = models.ManyToManyField(HazardousSubstanceEntity, related_name="hazardous_substances")

    hash_signature = models.CharField(max_length=256, null=True, blank=True)  # Blockchain readiness

    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp
    version = models.IntegerField(default=1)  # Versioning

    def __str__(self):
        return f"Material Composition for {self.battery_chemistry}"
