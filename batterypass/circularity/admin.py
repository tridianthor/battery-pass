from django.contrib import admin
from dpp_admin.admin import dpp_admin
from .models import PostalAddress, ComponentEntity, SparePartSupplierEntity
from .models import SafetyMeasuresEntity, RecycledContentEntity, EndOfLifeInformationEntity
from .models import DismantlingAndRemovalDocumentation, Circularity

class PostalAddressAdmin(admin.ModelAdmin):
    list_display = ('street_address', 'postal_code', 'country', 'created_at', 'version')
    list_filter = ('country', 'created_at')
    search_fields = ('street_address', 'postal_code')

dpp_admin.register(PostalAddress, PostalAddressAdmin)

class ComponentEntityAdmin(admin.ModelAdmin):
    list_display = ('part_name', 'part_number', 'created_at', 'version')
    list_filter = ('created_at', 'version')
    search_fields = ('part_name', 'part_number')

dpp_admin.register(ComponentEntity, ComponentEntityAdmin)

class SparePartSupplierEntityAdmin(admin.ModelAdmin):
    list_display = ('name_of_supplier', 'email_address_of_supplier', 'created_at', 'version')
    list_filter = ('created_at', 'version')
    search_fields = ('name_of_supplier', 'email_address_of_supplier')

dpp_admin.register(SparePartSupplierEntity, SparePartSupplierEntityAdmin)

class SafetyMeasuresEntityAdmin(admin.ModelAdmin):
    list_display = ('safety_instructions', 'created_at', 'version')
    list_filter = ('created_at', 'version')

dpp_admin.register(SafetyMeasuresEntity, SafetyMeasuresEntityAdmin)

class RecycledContentEntityAdmin(admin.ModelAdmin):
    list_display = ('pre_consumer_share' ,'recycled_material' ,'post_consumer_share' ,'created_at', 'version')
    list_filter = ('created_at', 'version')
    search_fields = ('recycled_material',)

dpp_admin.register(RecycledContentEntity, RecycledContentEntityAdmin)

class EndOfLifeInformationEntityAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'version')
    list_filter = ('created_at', 'version')

dpp_admin.register(EndOfLifeInformationEntity, EndOfLifeInformationEntityAdmin)

class DismantlingAndRemovalDocumentationAdmin(admin.ModelAdmin):
    list_display = ('document_type', 'created_at', 'version')
    list_filter = ('created_at', 'version')
    search_fields = ('document_type', 'document_url')

dpp_admin.register(DismantlingAndRemovalDocumentation, DismantlingAndRemovalDocumentationAdmin)

class CircularityAdmin(admin.ModelAdmin):
    list_display = ('safety_measures', 'renewable_content', 'created_at', 'version')
    list_filter = ('created_at', 'version')
    search_fields = ('safety_measures', 'renewable_content')

dpp_admin.register(Circularity, CircularityAdmin)
