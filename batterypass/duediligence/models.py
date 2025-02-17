from django.db import models

import uuid

# Create your models here.
class SupplyChainDueDiligence(models.Model):
    id = models.BigAutoField(primary_key=True)
    supply_chain_due_diligence_report = models.TextField(null=False)
    third_party_assurances = models.TextField(null=False)
    supply_chain_indices = models.FloatField(null=False, default=0)