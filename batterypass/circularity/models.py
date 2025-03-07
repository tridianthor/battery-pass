from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class DocumentType(models.TextChoices):
    BILL_OF_MATERIAL = "BillOfMaterial", "Bill of Material"
    MODEL_3D = "Model3D", "Model 3D"
    DISMANTLING_MANUAL = "DismantlingManual", "Dismantling Manual"
    REMOVAL_MANUAL = "RemovalManual", "Removal Manual"
    OTHER_MANUAL = "OtherManual", "Other Manual"
    DRAWING = "Drawing", "Drawing"


class RecycledMaterial(models.TextChoices):
    COBALT = "Cobalt", "Cobalt"
    NICKEL = "Nickel", "Nickel"
    LITHIUM = "Lithium", "Lithium"
    LEAD = "Lead", "Lead"


class PostalAddress(models.Model):
    id_short = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    semantic_id = models.URLField(blank=True, null=True)

    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    street_address = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    version = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.street_address}, {self.postal_code}, {self.country}"


class ComponentEntity(models.Model):
    id_short = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    semantic_id = models.URLField(blank=True, null=True)

    part_name = models.CharField(max_length=255)
    part_number = models.CharField(max_length=100, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    version = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.part_name} ({self.part_number})"


class SparePartSupplierEntity(models.Model):
    id_short = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    semantic_id = models.URLField(blank=True, null=True)

    name_of_supplier = models.CharField(max_length=255)
    address_of_supplier = models.ForeignKey(PostalAddress, on_delete=models.CASCADE)
    email_address_of_supplier = models.EmailField()
    supplier_web_address = models.URLField()
    components = models.ManyToManyField(ComponentEntity, related_name="suppliers")

    created_at = models.DateTimeField(auto_now_add=True)
    version = models.IntegerField(default=1)

    def __str__(self):
        return self.name_of_supplier


class SafetyMeasuresEntity(models.Model):
    id_short = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    semantic_id = models.URLField(blank=True, null=True)

    safety_instructions = models.FileField(max_length=255)
    extinguishing_agent = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)
    version = models.IntegerField(default=1)

    def __str__(self):
        return f"Safety Instructions: {self.safety_instructions}"


class RecycledContentEntity(models.Model):
    id_short = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    semantic_id = models.URLField(blank=True, null=True)

    pre_consumer_share = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )  # Ensuring % between 0-100
    recycled_material = models.CharField(max_length=50, choices=RecycledMaterial.choices)
    post_consumer_share = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )  # Ensuring % between 0-100

    created_at = models.DateTimeField(auto_now_add=True)
    version = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.recycled_material}: Pre-{self.pre_consumer_share}% | Post-{self.post_consumer_share}%"


class EndOfLifeInformationEntity(models.Model):
    id_short = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    semantic_id = models.URLField(blank=True, null=True)

    waste_prevention = models.FileField(max_length=255)
    separate_collection = models.FileField(max_length=255)
    information_on_collection = models.FileField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    version = models.IntegerField(default=1)

    def __str__(self):
        return f"Waste Prevention: {self.waste_prevention}"


class DismantlingAndRemovalDocumentation(models.Model):
    id_short = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    semantic_id = models.URLField(blank=True, null=True)

    document_type = models.CharField(max_length=50, choices=DocumentType.choices)
    mime_type = models.CharField(max_length=50)
    document_url = models.URLField()

    created_at = models.DateTimeField(auto_now_add=True)
    version = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.document_type} - {self.document_url}"


class Circularity(models.Model):
    id_short = models.CharField(max_length=255, unique=True, default=uuid.uuid4)  # AAS-compatible ID
    semantic_id = models.URLField(blank=True, null=True)  # Standardized reference

    circularity_id = models.CharField(max_length=255, unique=True)  # Standardized identifier
    dismantling_and_removal_information = models.ManyToManyField(
        DismantlingAndRemovalDocumentation, related_name="circularities"
    )
    spare_part_sources = models.ManyToManyField(SparePartSupplierEntity, related_name="circularities")
    recycled_content = models.ManyToManyField(RecycledContentEntity, related_name="circularities")
    safety_measures = models.ForeignKey(SafetyMeasuresEntity, on_delete=models.CASCADE)
    end_of_life_information = models.ForeignKey(EndOfLifeInformationEntity, on_delete=models.CASCADE)
    renewable_content = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    hash_signature = models.CharField(max_length=256, null=True, blank=True)  # Blockchain readiness

    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp
    version = models.IntegerField(default=1)  #
