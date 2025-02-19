from django.urls import path

from . import views
from .views import LabelingEntityAutoComplete

urlpatterns = [
    path('labeling/', views.labeling, name='labeling'),
    path('labeling/delete/<int:pk>', views.delete_labeling, name='labeling_delete'),
    path('labeling/entity/', views.labeling_entity, name='labeling_entity'),
    path('labeling/entity/delete/<int:pk>', views.delete_labeling_entity, name='labeling_entity_delete'),
    path('labeling/form/', views.labeling_form, name='labeling_form'),
    path('labeling/entity/form/', views.labeling_entity_form, name='labeling_entity_form'),
    path('labels-autocomplete/', LabelingEntityAutoComplete.as_view(), name='labels-autocomplete'), 
]