from django.db import models
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from common.models import ContactInformation

class HazardousSubstanceClassCharacteristic(models.TextChoices):
    ACUTE_TOXICITY = "AcuteToxicity", "Acute Toxicity"
    SKIN_CORROSION_OR_IRRITATION = "SkinCorrosionOrIrritation", "Skin Corrosion or Irritation"
    EYE_DAMAGE_OR_IRRITATION = "EyeDamageOrIrritation", "Eye Damage or Irritation"
    CARCINOGENIC = "Carcinogenic", "Carcinogenic" 
    SKIN_IRRITATION = "SkinIrritation", "Skin Irritation" 
    SKIN_EYE_IRRITANT = "Skin/EyeIrritant", "Skin/Eye Irritant" 
    CORROSIVE = "Corrosive", "Corrosive" 
    RESPIRATORY_SENSITIZER = "RespiratorySensitizer", "Respiratory Sensitizer"
    REPRODUCTIVE_TOXICITY = "ReproductiveToxicity", "Reproductive Toxicity"
    MUTAGENIC = "Mutagenic", "Mutagenic"

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



class ESGPerformanceSummary(models.TextChoices):
    HIGH = "High", "High ESG Compliance"
    MEDIUM = "Medium", "Medium ESG Compliance"
    LOW = "Low", "Low ESG Compliance"
    REPORTED = "Reported", "Reported but not classified"

class ESGPerformance(models.Model):
    id_short = models.CharField(max_length=255, unique=True, default=uuid.uuid4)

    # New Summary Field
    esg_performance_summary = models.CharField(
        max_length=50, choices=ESGPerformanceSummary.choices, default=ESGPerformanceSummary.REPORTED
    )

    # Detailed Breakdown Fields
    CARBON_CHOICES = [("Low", "Low"), ("Moderate", "Moderate"), ("High", "High"), ("Reported", "Reported")]
    carbon_footprint = models.CharField(max_length=50, choices=CARBON_CHOICES, default="Reported")

    RENEWABLE_CHOICES = [("0-25%", "0-25%"), ("26-50%", "26-50%"), ("51-75%", "51-75%"), ("76-100%", "76-100%"), ("Reported", "Reported")]
    renewable_energy_use = models.CharField(max_length=50, choices=RENEWABLE_CHOICES, default="Reported")

    WATER_CHOICES = [("Minimal", "Minimal"), ("Moderate", "Moderate"), ("Excessive", "Excessive"), ("Reported", "Reported")]
    water_consumption = models.CharField(max_length=100, choices=WATER_CHOICES, default="Reported")

    SOCIAL_CHOICES = [("Fair trade certified", "Fair trade certified"), ("Ethical sourcing", "Ethical sourcing"), ("No certification", "No certification"), ("Reported", "Reported")]
    social_impact = models.CharField(max_length=255, choices=SOCIAL_CHOICES, default="Reported")

    WORKER_SAFETY_CHOICES = [("High", "High"), ("Medium", "Medium"), ("Low", "Low"), ("Reported", "Reported")]
    worker_safety_standards = models.CharField(max_length=100, choices=WORKER_SAFETY_CHOICES, default="Reported")

    GOVERNANCE_CHOICES = [("ISO 14001", "ISO 14001"), ("EU Battery Directive", "EU Battery Directive"), ("REACH Certified", "REACH Certified"), ("No compliance", "No compliance"), ("Reported", "Reported")]
    governance_compliance = models.CharField(max_length=255, choices=GOVERNANCE_CHOICES, default="Reported")

    recycling_efficiency = models.CharField(max_length=50, choices=RENEWABLE_CHOICES, default="Reported")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ESG Performance: {self.esg_performance_summary}"   
    

class MaterialComposition(models.Model):
    id_short = models.CharField(max_length=255, unique=True, default=uuid.uuid4)  # AAS-compatible ID
    semantic_id = models.URLField(blank=True, null=True)  # Standardized reference

    material_composition_id = models.CharField(max_length=255, unique=True)  # Standardized identifier
    battery_chemistry = models.ForeignKey(
        BatteryChemistryEntity,
        on_delete=models.CASCADE,
        default=1  # ✅ Temporary default value (Ensure ID 1 exists in `BatteryChemistryEntity`)
    )
    battery_materials = models.ManyToManyField(BatteryMaterialEntity, related_name="materials")
    hazardous_substances = models.ManyToManyField(HazardousSubstanceEntity, related_name="hazardous_substances")

    # Adding First & Second Traced Material as ForeignKeys
    first_traced_material = models.ForeignKey(
        BatteryMaterialEntity, on_delete=models.SET_NULL, null=True, blank=True, related_name="first_traced"
    )
    second_traced_material = models.ForeignKey(
        BatteryMaterialEntity, on_delete=models.SET_NULL, null=True, blank=True, related_name="second_traced"
    )
    traceability = models.BooleanField(default=False)  # Whether the material is traceable
    tracing_period_start = models.DateField(null=True, blank=True)  # Start of traceability
    tracing_period_end = models.DateField(null=True, blank=True)  # End of traceability


    physical_amount = models.FloatField(
        validators=[MinValueValidator(0)], null=True, blank=True
    )  # Amount of material physically present
    traced_amount = models.FloatField(
        validators=[MinValueValidator(0)], null=True, blank=True
    )  # Amount of material that has been traced

    # ESG Summary Field
    esg_performance_summary = models.CharField(
        max_length=50, choices=ESGPerformanceSummary.choices, default=ESGPerformanceSummary.REPORTED
    )

    # Link to Detailed ESG Performance Model
    esg_performance = models.ForeignKey(ESGPerformance, on_delete=models.SET_NULL, null=True, blank=True)

    # Instead of storing manufacturer_name & manufacturer_country, 
    # we reference ContactInformation from the common app:
    manufacturer = models.ForeignKey(
        ContactInformation,
        on_delete=models.CASCADE,
        null=True,
        related_name="battery_materials",
        help_text="Which company produced these cells?"
    )

    hash_signature = models.CharField(max_length=256, null=True, blank=True)  # Blockchain readiness

    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp
    version = models.IntegerField(default=1)  # Versioning

    def __str__(self):
        return f"Material Composition for {self.battery_chemistry}"
