from django.db import models
from django.core.validators import MinValueValidator
from django.core.files.base import ContentFile
from django.conf import settings

import uuid
import django_filters
import qrcode
import os

from io import BytesIO
from utils.upload_util import Upload

from duediligence.models import SupplyChainDueDiligence
from labeling.models import Labeling
from carbonfootprints.models import CarbonFootprintForBatteries
from materials.models import MaterialComposition
from circularity.models import Circularity
from performance.models import PerformanceAndDurability
from common.models import ContactInformation
from batterycell.models import BatteryCell

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
    id_short = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    semantic_id = models.URLField(blank=True, null=True)
    
    address_country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    street_address = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp
    version = models.IntegerField(default=1)  # Versioning
    
    def __str__(self):
        return f"{self.street_address}, {self.postal_code}, {self.address_country}"


class GeneralProductInformation(models.Model):
    id_short = models.CharField(max_length=255, unique=True, default=uuid.uuid4)  # AAS compatible identifier
    semantic_id = models.URLField(blank=True, null=True)  # Semantic reference for standardization

    battery_id = models.CharField(max_length=255, unique=True)  # Standardized identifier
    product_identifier = models.CharField(max_length=255, unique=True)
    battery_model_number = models.CharField(max_length=255, null=True) # Model Number should not be part of 
    battery_passport_identifier = models.CharField(max_length=255, unique=True)
    
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)
    
    battery_category = models.CharField(
        max_length=50, choices=BatteryCategoryEnum.choices
    )
    
    battery_cell = models.ForeignKey(
        BatteryCell,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="batterycell_infos"
    )

    manufacturer_information = models.ForeignKey(
        ContactInformation, on_delete=models.CASCADE, related_name="manufacturers_info"
    )

    manufacturing_date = models.DateField()
    battery_status = models.CharField(
        max_length=50, choices=BatteryStatusEnumeration.choices
    )
    battery_mass = models.FloatField(validators=[MinValueValidator(0)])  # Ensuring no negative values
    
    operator_information = models.ForeignKey(
        ContactInformation, on_delete=models.CASCADE, related_name="operators"
    )
    putting_into_service = models.DateField()
    warranty_period = models.DateField()
    
    due_diligence = models.OneToOneField(
        SupplyChainDueDiligence, on_delete=models.CASCADE, related_name="due_diligence"
    )
    
    label = models.OneToOneField(
        Labeling, on_delete=models.CASCADE, related_name="label"
    )
    
    carbon_footprint = models.OneToOneField(
        CarbonFootprintForBatteries, on_delete=models.CASCADE, related_name="carbon_footprint"
    )
    
    material_composition = models.OneToOneField(
        MaterialComposition, on_delete=models.CASCADE, related_name="material_composition"
    )
    
    circularity = models.OneToOneField(
        Circularity, on_delete=models.CASCADE, related_name="circularity"
    )
    
    performance = models.OneToOneField(
        PerformanceAndDurability, on_delete=models.CASCADE, related_name="performance"
    )
    
    hash_signature = models.CharField(max_length=256, null=True, blank=True)  # Blockchain readiness

    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp
    version = models.IntegerField(default=1)  # Versioning

    def __str__(self):
        return self.product_identifier
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.qr_code:
            filename = f"qr_{self.id_short}.png"
            qr_code_url = generate_qr_code(f"{settings.SITE_URL}/summary/{self.battery_passport_identifier}", filename)
            self.qr_code = qr_code_url
            super().save(*args, **kwargs)

def generate_qr_code(data, filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Save the QR code image to a BytesIO buffer
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    file_path = os.path.join(settings.MEDIA_ROOT, f"{filename}")
    with open(file_path, 'wb') as f:
        f.write(buffer.getvalue())

    return os.path.join(settings.MEDIA_URL, f"{filename}")

def regenerate_qr_code(pk=None, code=None):
    if pk is not None:
        product = GeneralProductInformation.objects.get(pk=pk)
    else:
        product = GeneralProductInformation.objects.get(battery_passport_identifier=code)
    
    filename = f"qr_{product.id_short}.png"
    qr_code_url = generate_qr_code(f"{settings.SITE_URL}/summary/{product.battery_passport_identifier}", filename)
    product.qr_code = qr_code_url
    product.save()

class GeneralProductInfoFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    class Meta:
        model = GeneralProductInformation
        fields = ['battery_passport_identifier']
    
    def filter_search(self, queryset, name, value):
        return queryset.filter(battery_passport_identifier__icontains=value)
    
