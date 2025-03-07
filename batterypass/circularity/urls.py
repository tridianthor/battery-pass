from django.urls import path

from . import views
from .views import ComponentsAutocomplete, DismantlingAndRemovalDocumentationAutocomplete, SparePartSupplierAutocomplete, RecycledContentAutocomplete

urlpatterns = [
    path('postal-addresses/', views.postal_addresses, name='postal-addresses'),
    path('postal-addresses/delete/<int:pk>', views.delete_postal_address, name='delete-postal-address'),
    path('postal-addresses/form/', views.insert_update_postal_address, name='insert-postal-address'),
    path('postal-addresses/form/<int:pk>', views.insert_update_postal_address, name='update-postal-address'),
    path('component-entities/', views.component_entities, name='component-entities'),
    path('component-entities/delete/<int:pk>', views.delete_component_entity, name='delete-component-entity'),
    path('component-entities/form/', views.insert_update_component_entity, name='insert-component-entity'),
    path('component-entities/form/<int:pk>', views.insert_update_component_entity, name='update-component-entity'),
    path('components-autocomplete', ComponentsAutocomplete.as_view(), name='components-autocomplete'),
    path('dismantling-and-removal-documentation-autocomplete', DismantlingAndRemovalDocumentationAutocomplete.as_view(), name='dismantling-and-removal-documentation-autocomplete'),
    path('spare-part-supplier-autocomplete', SparePartSupplierAutocomplete.as_view(), name='spare-part-supplier-autocomplete'),
    path('recycled-content-autocomplete', RecycledContentAutocomplete.as_view(), name='recycled-content-autocomplete'),
]