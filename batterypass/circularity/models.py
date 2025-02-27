from django.db import models

import uuid 
# Create your models here.

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
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    street_address = models.CharField(max_length=255)
    insert_date = models.DateTimeField(auto_now_add=True, editable=False)
    update_date = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"{self.street_address}, {self.postal_code}, {self.country}"


class ComponentEntity(models.Model):
    part_name = models.CharField(max_length=255)
    part_number = models.CharField(max_length=100, unique=True)
    insert_date = models.DateTimeField(auto_now_add=True, editable=False)
    update_date = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"{self.part_name} ({self.part_number})"


class SparePartSupplierEntity(models.Model):
    name_of_supplier = models.CharField(max_length=255)
    address_of_supplier = models.ForeignKey(PostalAddress, on_delete=models.CASCADE)
    email_address_of_supplier = models.EmailField()
    supplier_web_address = models.TextField(null=False)
    components = models.ManyToManyField(ComponentEntity, related_name="suppliers")
    insert_date = models.DateTimeField(auto_now_add=True, editable=False)
    update_date = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.name_of_supplier


class SafetyMeasuresEntity(models.Model):
    safety_instructions = models.TextField(null=False) #this field stores filename
    extinguishing_agent = models.JSONField()
    insert_date = models.DateTimeField(auto_now_add=True, editable=False)
    update_date = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"Safety Instructions: {self.safety_instructions}"


class RecycledContentEntity(models.Model):
    pre_consumer_share = models.FloatField()
    recycled_material = models.CharField(max_length=50, choices=RecycledMaterial.choices)
    post_consumer_share = models.FloatField()
    insert_date = models.DateTimeField(auto_now_add=True, editable=False)
    update_date = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"{self.recycled_material}: Pre-{self.pre_consumer_share}% | Post-{self.post_consumer_share}%"


class EndOfLifeInformationEntity(models.Model):
    waste_prevention = models.TextField(null=False) #this field stores filename
    separate_collection = models.TextField(null=False) #this field stores filename
    information_on_collection = models.TextField(null=False) #this field stores filename
    insert_date = models.DateTimeField(auto_now_add=True, editable=False)
    update_date = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"Waste Prevention: {self.waste_prevention}"


class DismantlingAndRemovalDocumentation(models.Model):
    document_type = models.CharField(max_length=50, choices=DocumentType.choices)
    mime_type = models.CharField(max_length=50)
    document_url = models.TextField(null=False) #this field stores filename
    insert_date = models.DateTimeField(auto_now_add=True, editable=False)
    update_date = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"{self.document_type} - {self.document_url}"


class Circularity(models.Model):
    id = models.BigAutoField(primary_key=True)
    dismantling_and_removal_information = models.ManyToManyField(
        DismantlingAndRemovalDocumentation, related_name="circularities"
    )
    spare_part_sources = models.ManyToManyField(SparePartSupplierEntity, related_name="circularities")
    recycled_content = models.ManyToManyField(RecycledContentEntity, related_name="circularities")
    safety_measures = models.ForeignKey(SafetyMeasuresEntity, on_delete=models.CASCADE)
    end_of_life_information = models.ForeignKey(EndOfLifeInformationEntity, on_delete=models.CASCADE)
    renewable_content = models.FloatField()
    insert_date = models.DateTimeField(auto_now_add=True, editable=False)
    update_date = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"Circularity - Renewable Content: {self.renewable_content}%"
