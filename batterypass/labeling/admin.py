from django.contrib import admin
from dpp_admin.admin import dpp_admin
from .models import Labeling, LabelingEntity
# Register your models here.

class LabelingAdmin(admin.ModelAdmin):
    list_display = ("labeling_id", "declaration_of_conformity", "result_of_test_report", "created_at", "version")
    search_fields = ("labeling_id", "declaration_of_conformity", "result_of_test_report", "created_at", "version")
    list_filter = ("created_at", "version")

dpp_admin.register(Labeling, LabelingAdmin)

class LabelingEntityAdmin(admin.ModelAdmin):
    list_display = ("labeling_id", "labeling_symbol", "labeling_meaning", "labeling_subject", "created_at", "version")
    search_fields = ("labeling_id", "labeling_symbol", "labeling_meaning", "labeling_subject", "created_at", "version")
    list_filter = ("created_at", "version")

dpp_admin.register(LabelingEntity, LabelingEntityAdmin)