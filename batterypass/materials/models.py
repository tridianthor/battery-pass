from django.db import models

import uuid

# Create your models here.
""" class MaterialComposition(models.Model):
    material_composition_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    battery_chemistry_short_name = models.TextField(db_column='battery_chemistry__short_name', blank=True, null=True)  # Field renamed because it contained more than one '_' in a row.
    battery_chemistry_clear_name = models.TextField(db_column='battery_chemistry__clear_name', blank=True, null=True)  # Field renamed because it contained more than one '_' in a row.

class ComponentType(models.Model):
    component_id = models.TextField(primary_key=True)
    component_name = models.TextField()
    
class BatteryMaterialType(models.Model):
    battery_material_identifier = models.TextField(primary_key=True)
    material_composition_id = models.ForeignKey(MaterialComposition, on_delete=models.CASCADE)
    battery_material_location = models.OneToOneField(ComponentType, on_delete=models.CASCADE)
    battery_material_name = models.TextField()
    battery_material_mass = models.FloatField()
    is_critical_raw_material = models.BooleanField()

class HazardousSubstanceType(models.Model):
    hazardous_substance_identifier = models.TextField(primary_key=True)
    material_composition_id = models.ForeignKey(MaterialComposition, on_delete=models.CASCADE)
    hazardous_substance_class = models.TextField()
    hazardous_substance_name = models.TextField()
    hazardous_substance_concentration = models.FloatField()
    hazardous_substance_impact = models.TextField()
    hazardous_substance_location = models.OneToOneField(ComponentType, on_delete=models.CASCADE) """
    
class HazardousSubstanceClassCharacteristic(models.TextChoices):
    ACUTE_TOXICITY = "AcuteToxicity", "Acute Toxicity"
    SKIN_CORROSION_OR_IRRITATION = "SkinCorrosionOrIrritation", "Skin Corrosion or Irritation"
    EYE_DAMAGE_OR_IRRITATION = "EyeDamageOrIrritation", "Eye Damage or Irritation"

class BatteryLocationEntity(models.Model):
    component_name = models.CharField(max_length=255)
    component_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.component_name} ({self.component_id})" if self.component_id else self.component_name

class BatteryMaterialEntity(models.Model):
    battery_material_location = models.ForeignKey(BatteryLocationEntity, on_delete=models.CASCADE)
    battery_material_identifier = models.CharField(max_length=20, unique=True)
    battery_material_name = models.CharField(max_length=255)
    battery_material_mass = models.FloatField()
    is_critical_raw_material = models.BooleanField()

    def __str__(self):
        return f"{self.battery_material_name} ({self.battery_material_identifier})"

class HazardousSubstanceEntity(models.Model):
    hazardous_substance_class = models.CharField(
        max_length=50, choices=HazardousSubstanceClassCharacteristic.choices
    )
    hazardous_substance_name = models.CharField(max_length=255)
    hazardous_substance_concentration = models.FloatField()
    hazardous_substance_impact = models.JSONField()  # List of impacts stored as JSON
    hazardous_substance_location = models.ForeignKey(BatteryLocationEntity, on_delete=models.CASCADE)
    hazardous_substance_identifier = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.hazardous_substance_name} ({self.hazardous_substance_identifier})"

class BatteryChemistryEntity(models.Model):
    short_name = models.CharField(max_length=100, unique=True)
    clear_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.clear_name} ({self.short_name})"

class MaterialComposition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    battery_chemistry = models.ForeignKey(BatteryChemistryEntity, on_delete=models.CASCADE)
    battery_materials = models.ManyToManyField(BatteryMaterialEntity, related_name="materials")
    hazardous_substances = models.ManyToManyField(HazardousSubstanceEntity, related_name="hazardous_substances")

    def __str__(self):
        return f"Material Composition for {self.battery_chemistry}"
