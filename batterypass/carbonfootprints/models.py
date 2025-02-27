from django.db import models

import uuid
# Create your models here.

class LifecycleStage(models.TextChoices):
    RAW_MATERIAL_EXTRACTION = "RawMaterialExtraction", "Raw Material Extraction"
    MAIN_PRODUCTION = "MainProduction", "Main Production"
    DISTRIBUTION = "Distribution", "Distribution"
    RECYCLING = "Recycling", "Recycling"


class CarbonFootprintPerLifecycleStageEntity(models.Model):
    lifecycle_stage = models.CharField(
        max_length=50, choices=LifecycleStage.choices
    )
    carbon_footprint = models.FloatField()
    insert_date = models.DateTimeField(auto_now_add=True, editable=False)
    update_date = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"{self.lifecycle_stage} - {self.carbon_footprint} kgCO2"


class CarbonFootprintForBatteries(models.Model):
    id = models.BigAutoField(primary_key=True)
    battery_carbon_footprint = models.FloatField()
    carbon_footprint_per_lifecycle_stage = models.ManyToManyField(
        CarbonFootprintPerLifecycleStageEntity, related_name="batteries"
    )
    carbon_footprint_performance_class = models.CharField(max_length=255)
    carbon_footprint_study = models.TextField(null=False) #this field stores filename
    absolute_carbon_footprint = models.FloatField(null=True, blank=True)
    insert_date = models.DateTimeField(auto_now_add=True, editable=False)
    update_date = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"Battery Carbon Footprint: {self.battery_carbon_footprint} kgCO2"
