from django.urls import path

from . import views

urlpatterns = [
    path('carbon_footprint/', views.carbon_footprints, name='carbon_footprints'),
    path('carbon_footprint/form/', views.insert_carbon_footprints, name='insert_carbon_footprints'),
    path('carbon_footprint/form/<int:pk>', views.update_carbon_footprints, name='update_carbon_footprints'),
    path('carbon_footprint/delete/<int:pk>', views.delete_carbon_footprints, name='delete_carbon_footprints'),
    path('carbon_footprint_per_lifecycle_stage/', views.carbon_footprints_lifecycles, name='carbon_footprints_lifecycles'),
    path('carbon_footprint_per_lifecycle_stage/form/', views.insert_carbon_footprints_lifecycle, name='insert_carbon_footprints_lifecycle'),
    path('carbon_footprint_per_lifecycle_stage/form/<int:pk>', views.update_carbon_footprints_lifecycle, name='update_carbon_footprints_lifecycle'),
    path('carbon_footprint_per_lifecycle_stage/delete/<int:pk>', views.delete_carbon_footprints_lifecycle, name='delete_carbon_footprints_lifecycle'),
    path('cfperlifecyclese-autocomplete/', views.CarbonFootprintsLifecycleAutoComplete.as_view(), name='cfperlifecyclese-autocomplete'),
]