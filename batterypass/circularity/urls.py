from django.urls import path

from . import views
from .views import ComponentsAutocomplete, DismantlingAndRemovalDocumentationAutocomplete, SparePartSupplierAutocomplete, RecycledContentAutocomplete

urlpatterns = [
    path('postal-addresses/', views.postal_addresses, name='postal_addresses'),
    path('postal-addresses/delete/<int:pk>', views.delete_postal_address, name='delete_postal_address'),
    path('postal-addresses/form/', views.insert_update_postal_address, name='insert_postal_address'),
    path('postal-addresses/form/<int:pk>', views.insert_update_postal_address, name='update_postal_address'),
    path('component-entities/', views.component_entities, name='component_entities'),
    path('component-entities/delete/<int:pk>', views.delete_component_entity, name='delete_component_entity'),
    path('component-entities/form/', views.insert_update_component_entity, name='insert_component_entity'),
    path('component-entities/form/<int:pk>', views.insert_update_component_entity, name='update_component_entity'),
    path('components-autocomplete', ComponentsAutocomplete.as_view(), name='components_autocomplete'),
    path('dismantling-and-removal-documentation-autocomplete', DismantlingAndRemovalDocumentationAutocomplete.as_view(), name='dismantling_and_removal_documentation_autocomplete'),
    path('spare-part-supplier-autocomplete', SparePartSupplierAutocomplete.as_view(), name='spare_part_supplier_autocomplete'),
    path('recycled-content-autocomplete', RecycledContentAutocomplete.as_view(), name='recycled_content_autocomplete'),
]