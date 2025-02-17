from django.contrib import admin
from .models import Labeling, LabelingEntity
# Register your models here.

admin.site.register(Labeling)
admin.site.register(LabelingEntity)