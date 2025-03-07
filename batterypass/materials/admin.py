from django.contrib import admin
from .models import BatteryLocationEntity, BatteryMaterialEntity, HazardousSubstanceEntity
from .models import BatteryChemistryEntity, MaterialComposition
# Register your models here.

admin.site.register(BatteryLocationEntity)
admin.site.register(BatteryMaterialEntity)
admin.site.register(HazardousSubstanceEntity)
admin.site.register(BatteryChemistryEntity)
admin.site.register(MaterialComposition)