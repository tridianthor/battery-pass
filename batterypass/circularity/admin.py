from django.contrib import admin
from .models import PostalAddress, ComponentEntity, SparePartSupplierEntity
from .models import SafetyMeasuresEntity, RecycledContentEntity, EndOfLifeInformationEntity
from .models import DismantlingAndRemovalDocumentation, Circularity

admin.site.register(PostalAddress)
admin.site.register(ComponentEntity)
admin.site.register(SparePartSupplierEntity)
admin.site.register(SafetyMeasuresEntity)
admin.site.register(RecycledContentEntity)
admin.site.register(EndOfLifeInformationEntity)
admin.site.register(DismantlingAndRemovalDocumentation)
admin.site.register(Circularity)
