from django.db import models

# Create your models here.

class LabelingSubject(models.TextChoices):
    SEPARATE_COLLECTION = "SeparateCollection", "Separate Collection"
    HAZARDOUS_MATERIAL = "HazardousMaterial", "Hazardous Material"
    CARBON_FOOTPRINT = "CarbonFootPrint", "Carbon Footprint"
    EXTINGUISHING_AGENT = "ExtinguishingAgent", "Extinguishing Agent"
    
class LabelingEntity(models.Model):
    labeling_symbol = models.TextField() # File
    labeling_meaning = models.JSONField()  # original : langString
    labeling_subject = models.CharField(
        max_length=50, choices=LabelingSubject.choices
    )

    def __str__(self):
        return f"{self.labeling_subject}"

class Labeling(models.Model):
    id = models.BigAutoField(primary_key=True)
    declaration_of_conformity = models.TextField() # File
    result_of_test_report = models.TextField() # File
    labels = models.ManyToManyField(LabelingEntity, related_name="labelings")

    def __str__(self):
        return f"Labeling - Conformity: {self.declaration_of_conformity}"
