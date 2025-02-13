from django.db import models

import uuid
# Create your models here.

class BatteryCategoryEnum(models.TextChoices):
    LMT = "lmt", "LMT"
    EV = "ev", "EV"
    INDUSTRIAL = "industrial", "Industrial"
    STATIONARY = "stationary", "Stationary"


class BatteryStatusEnumeration(models.TextChoices):
    ORIGINAL = "Original", "Original"
    REPURPOSED = "Repurposed", "Repurposed"
    REUSED = "Reused", "Reused"
    REMANUFACTURED = "Remanufactured", "Remanufactured"
    WASTE = "Waste", "Waste"


class PostalAddressEntity(models.Model):
    address_country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    street_address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.street_address}, {self.postal_code}, {self.address_country}"


class ContactInformationEntity(models.Model):
    contact_name = models.CharField(max_length=255)
    postal_address = models.ForeignKey(PostalAddressEntity, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.contact_name


class GeneralProductInformation(models.Model):
    product_identifier = models.CharField(max_length=255, unique=True)
    battery_passport_identifier = models.CharField(max_length=255, unique=True)
    battery_category = models.CharField(
        max_length=50, choices=BatteryCategoryEnum.choices
    )
    manufacturer_information = models.ForeignKey(
        ContactInformationEntity, on_delete=models.CASCADE, related_name="manufacturers"
    )
    manufacturing_date = models.DateField()
    battery_status = models.CharField(
        max_length=50, choices=BatteryStatusEnumeration.choices
    )
    battery_mass = models.FloatField()
    manufacturing_place = models.ForeignKey(
        PostalAddressEntity, on_delete=models.CASCADE, related_name="manufacturing_places"
    )
    operator_information = models.ForeignKey(
        ContactInformationEntity, on_delete=models.CASCADE, related_name="operators"
    )
    putting_into_service = models.DateField()
    warranty_period = models.DateField()

    def __str__(self):
        return self.product_identifier