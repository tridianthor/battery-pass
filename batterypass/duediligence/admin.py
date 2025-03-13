from django.contrib import admin
from dpp_admin.admin import dpp_admin
from .models import SupplyChainDueDiligence
# Register your models here.

class DueDiligenceAdmin(admin.ModelAdmin):
    list_display = ('supply_chain_id', 'supply_chain_due_diligence_report', 'third_party_assurances', 'supply_chain_indices', 'hash_signature', 'created_at', 'version')
    search_fields = ('supply_chain_id', 'supply_chain_due_diligence_report', 'third_party_assurances', 'supply_chain_indices', 'hash_signature', 'created_at', 'version')
    list_filter = ('supply_chain_id', 'supply_chain_due_diligence_report', 'third_party_assurances', 'supply_chain_indices', 'hash_signature', 'created_at', 'version')
    ordering = ('supply_chain_id', 'supply_chain_due_diligence_report', 'third_party_assurances', 'supply_chain_indices', 'hash_signature', 'created_at', 'version')

dpp_admin.register(SupplyChainDueDiligence, DueDiligenceAdmin)


