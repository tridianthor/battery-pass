from django.db import models
from .types import LabelTypeField
from django.contrib.postgres.fields import ArrayField

import uuid

# Create your models here.

""" class Labeling(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    declaration_of_conformity = models.TextField()
    result_of_test_report = models.TextField()
    labels = ArrayField(LabelTypeField(), null=True, blank=True)
    
    def __str__(self):
        return f"{self.id}, {self.declaration_of_conformity}, {self.result_of_test_report}, {self.labels}" """
        
""" class LabelingTypes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    labeling_id = models.ForeignKey('labeling.Labeling', on_delete=models.CASCADE, related_name="labeling_types")
    labeling_symbol = models.TextField()
    labeling_meaning = models.TextField()
    labeling_subject = models.TextField() """

class LabelingSubject(models.TextChoices):
    SEPARATE_COLLECTION = "SeparateCollection", "Separate Collection"
    HAZARDOUS_MATERIAL = "HazardousMaterial", "Hazardous Material"
    CARBON_FOOTPRINT = "CarbonFootPrint", "Carbon Footprint"
    EXTINGUISHING_AGENT = "ExtinguishingAgent", "Extinguishing Agent"
    
class LabelingEntity(models.Model):
    labeling_symbol = models.URLField()
    labeling_meaning = models.TextField()  # Converted from LangString (assumed to be a string field)
    labeling_subject = models.CharField(
        max_length=50, choices=LabelingSubject.choices
    )

    def __str__(self):
        return f"{self.labeling_subject} - {self.labeling_symbol}"

class Labeling(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    declaration_of_conformity = models.URLField()
    result_of_test_report = models.URLField()
    labels = models.ManyToManyField(LabelingEntity, related_name="labelings")

    def __str__(self):
        return f"Labeling - Conformity: {self.declaration_of_conformity}"
