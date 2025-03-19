# common/models.py

import uuid
from django.db import models
from django_countries.fields import CountryField

class Address(models.Model):
    id_short = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    semantic_id = models.URLField(blank=True, null=True)

    # Use CountryField from django-countries
    country = CountryField(blank_label='(select country)')

    postal_code = models.CharField(max_length=20)
    street_address = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    version = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.street_address}, {self.postal_code}, {self.country.name}"

class ContactType(models.TextChoices):
    """
    Enumerated roles for a contact, so each lifecycle stage
    can reference one main contact with a specific role.
    """
    MINING = "mining", "Mining"
    CELL_PRODUCTION = "cell_production", "Cell Production"
    MANUFACTURING = "manufacturing", "Manufacturing"
    DISTRIBUTION = "distribution", "Distribution"
    RECYCLING = "recycling", "Recycling"
    # Add others as needed


class ContactInformation(models.Model):
    """
    A single main contact for a given lifecycle stage or function.
    """
    id_short = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    semantic_id = models.URLField(blank=True, null=True)

    # The company's name
    company_name = models.CharField(max_length=255,null=True,blank=True)

    # The person's  name
    contact_name = models.CharField(max_length=255,null=True,blank=True)

    # A single role for this contact, e.g. "mining" or "manufacturing"
    contact_role = models.CharField(
        max_length=50,
        choices=ContactType.choices
    )

    # A single address for this contact
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    # Optional fields for phone, email, etc.
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    version = models.IntegerField(default=1)

    def __str__(self):
        # You can customize how this contact is displayed
        return f"{self.company_name} ({self.get_contact_role_display()})"