from django.contrib import admin
from .models import CarbonFootprintForBatteries, CarbonFootprintPerLifecycleStageEntity
# Register your models here.

admin.site.register(CarbonFootprintForBatteries)
admin.site.register(CarbonFootprintPerLifecycleStageEntity)
