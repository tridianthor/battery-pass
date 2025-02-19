from django.db import models

# Create your models here.
class SupplyChainDueDiligence(models.Model):
    id = models.BigAutoField(primary_key=True)
    supply_chain_due_diligence_report = models.TextField(null=False)
    third_party_assurances = models.TextField(null=False)
    supply_chain_indices = models.FloatField(null=False, default=0)
    insert_date = models.DateTimeField(auto_now_add=True, editable=False)
    update_date = models.DateTimeField(auto_now=True, editable=False)