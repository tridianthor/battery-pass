from django.db import models
import uuid
from django.conf import settings
class LabelingSubject(models.TextChoices):
    SEPARATE_COLLECTION = "SeparateCollection", "Separate Collection"
    HAZARDOUS_MATERIAL = "HazardousMaterial", "Hazardous Material"
    CARBON_FOOTPRINT = "CarbonFootPrint", "Carbon Footprint"
    EXTINGUISHING_AGENT = "ExtinguishingAgent", "Extinguishing Agent"

class LabelingEntity(models.Model):
    id_short = models.CharField(max_length=255, unique=True, default=uuid.uuid4)  # AAS-compatible ID
    semantic_id = models.URLField(blank=True, null=True)  # Standardized reference

    labeling_id = models.CharField(max_length=255, unique=True)  # Standardized identifier
    labeling_symbol = models.FileField(max_length=255)  # URL to symbol image
    labeling_meaning = models.TextField()  # Label description
    labeling_subject = models.CharField(max_length=50, choices=LabelingSubject.choices)

    hash_signature = models.CharField(max_length=256, null=True, blank=True)  # Blockchain readiness

    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp
    version = models.IntegerField(default=1)  # Versioning

    def __str__(self):
        return f"{self.labeling_subject} - {self.labeling_symbol}"
        
class Labeling(models.Model):
    id_short = models.CharField(max_length=255, unique=True, default=uuid.uuid4)  # AAS-compatible ID
    semantic_id = models.URLField(blank=True, null=True)  # Standardized reference

    labeling_id = models.CharField(max_length=255, unique=True)  # Standardized identifier
    declaration_of_conformity = models.FileField(max_length=255)  # URL to conformity declaration
    result_of_test_report = models.FileField(max_length=255)  # URL to test report
    labels = models.ManyToManyField(LabelingEntity, related_name="labelings")

    hash_signature = models.CharField(max_length=256, null=True, blank=True)  # Blockchain readiness

    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp
    version = models.IntegerField(default=1)  # Versioning

    def __str__(self):
        return f"Labeling - Conformity: {self.declaration_of_conformity}"
