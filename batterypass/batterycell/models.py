# batterycell/models.py

import uuid
from django.db import models
from django_countries.fields import CountryField

from common.models import ContactInformation

class CellFormFactor(models.TextChoices):
    CYLINDRICAL_18650 = "Cylindrical (18650)", "Cylindrical (18650)"
    CYLINDRICAL_21700 = "Cylindrical (21700)", "Cylindrical (21700)"
    POUCH = "pouch", "Pouch"
    PRISMATIC = "prismatic", "Prismatic"
    OTHER = "other", "Other"

class BatteryChemistry(models.TextChoices):
    LFP = "LFP", "Lithium Iron Phosphate (LFP)"
    NMC622 = "NMC622", "NMC (6:2:2)"
    NMC811 = "NMC811", "NMC (8:1:1)"
    NCA = "NCA", "Nickel Cobalt Aluminum (NCA)"
    OTHER = "other", "Other"

class BatteryCell(models.Model):
    """
    Represents a battery cell or batch of identical cells,
    referencing the manufacturer from common.ContactInformation.
    """
    id_short = models.CharField(
        max_length=255,
        unique=True,
        default=uuid.uuid4
    )
    semantic_id = models.URLField(blank=True, null=True)

    cell_id = models.CharField(
        max_length=100,
        unique=True,
        help_text="A user-friendly ID for the cell or cell batch."
    )
    cell_type = models.CharField(
        max_length=30,
        choices=CellFormFactor.choices
    )
    number_of_cells = models.PositiveIntegerField(
        default=1,
        help_text="If grouping multiple identical cells under this record."
    )

    # Instead of storing manufacturer_name & manufacturer_country, 
    # we reference ContactInformation from the common app:
    manufacturer = models.ForeignKey(
        ContactInformation,
        on_delete=models.CASCADE,
        null=True,
        related_name="battery_cells",
        help_text="Which company produced these cells?"
    )

    manufacturing_date = models.DateField(
        blank=True,
        null=True,
        help_text="Date of manufacturing (if known)."
    )
    chemistry = models.CharField(
        max_length=10,
        choices=BatteryChemistry.choices,
        default=BatteryChemistry.OTHER
    )
    nominal_voltage = models.FloatField(
        help_text="Nominal voltage (V) per cell."
    )
    rated_capacity_ah = models.FloatField(
        help_text="Rated capacity (Ah) per cell."
    )

    created_at = models.DateTimeField(auto_now_add=True)
    version = models.IntegerField(default=1)

    def __str__(self):
        # For the admin or wherever a string is needed,
        # we reference cell_id and cell_type for clarity.
        return f"{self.cell_id} ({self.get_cell_type_display()})"
