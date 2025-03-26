from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
import django_filters
class SupplyChainDueDiligence(models.Model):
    id_short = models.CharField(max_length=255, unique=True, default=uuid.uuid4)  # AAS-compatible ID
    semantic_id = models.URLField(blank=True, null=True)  # Standardized reference

    supply_chain_id = models.CharField(max_length=255, unique=True)  # Standardized identifier
    supply_chain_due_diligence_report = models.FileField(
        upload_to='supplychain/due_diligence_report',
        max_length=255)  # URL to due diligence report
    third_party_assurances = models.FileField(
        upload_to='supplychain/third_party_assurances',
        null=True, blank=True)  # Optional third-party validation
    supply_chain_indices = models.FloatField(
        null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )  # Percentage-based index (0-100%)

    # New field for Sustainability Report
    sustainability_report = models.FileField(
        upload_to='supplychain/sustainability_reports/', null=True, blank=True,
        help_text="Upload the sustainability report PDF file."
    )


    hash_signature = models.CharField(max_length=256, null=True, blank=True)  # Blockchain readiness

    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp
    version = models.IntegerField(default=1)  # Versioning

    def __str__(self):
        return f"Supply Chain Due Diligence Report: {self.supply_chain_due_diligence_report}"
    
class SupplyChainDueDiligenceFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    class Meta:
        model = SupplyChainDueDiligence
        fields = ['supply_chain_indices']
    
    def filter_search(self, queryset, name, value):
        return queryset.filter(supply_chain_due_diligence_report__icontains=value)