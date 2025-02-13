from django.db import models

import uuid

# Create your models here.
class SupplyChainDueDiligence(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    supply_chain_due_diligence_report = models.URLField()
    third_party_aussurances = models.URLField(null=True, blank=True)
    supply_chain_indicies = models.FloatField(null=True, blank=True)