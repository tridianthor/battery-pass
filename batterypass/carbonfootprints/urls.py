from django.urls import path

from . import views

urlpatterns = [
    path('carbonfootprints/', views.carbon_footprints, name='carbon_footprints'),
    path('carbonfootprints/form/', views.insert_carbon_footprints, name='insert_carbon_footprints'),
    path('carbonfootprints/form/<int:pk>', views.update_carbon_footprints, name='update_carbon_footprints'),
    path('carbonfootprints/delete/<int:pk>', views.delete_carbon_footprints, name='delete_carbon_footprints'),
    path('carbonfootprints/lifecycles/', views.carbon_footprints_lifecycles, name='carbon_footprints_lifecycles'),
    path('carbonfootprints/lifecycles/form/', views.insert_carbon_footprints_lifecycle, name='insert_carbon_footprints_lifecycle'),
    path('carbonfootprints/lifecycles/form/<int:pk>', views.update_carbon_footprints_lifecycle, name='update_carbon_footprints_lifecycle'),
    path('carbonfootprints/lifecycles/delete/<int:pk>', views.delete_carbon_footprints_lifecycle, name='delete_carbon_footprints_lifecycle'),
    path('cfperlifecyclese-autocomplete/', views.CarbonFootprintsLifecycleAutoComplete.as_view(), name='cfperlifecyclese-autocomplete'),
]