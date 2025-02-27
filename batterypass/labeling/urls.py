from django.urls import path

from utils.pdf import view_pdf

from . import views
from .views import LabelingEntityAutoComplete

urlpatterns = [
    path('labeling/', views.labeling, name='labeling'),
    path('labeling/delete/<int:pk>', views.delete_labeling, name='labeling_delete'),
    path('labeling/entity/', views.labeling_entity, name='labeling_entity'),
    path('labeling/entity/delete/<int:pk>', views.delete_labeling_entity, name='labeling_entity_delete'),
    path('labeling/form/', views.insert_labeling, name='insert_labeling'),
    path('labeling/form/<int:pk>', views.update_labeling, name='update_labeling'),
    path('labeling/entity/form/', views.insert_labeling_entity, name='insert_labeling_entity'),
    path('labeling/entity/form/<int:pk>', views.update_labeling_entity, name='update_labeling_entity'),
    path('labels-autocomplete/', LabelingEntityAutoComplete.as_view(), name='labels-autocomplete'), 
    path('labeling/pdf/<path:folder>/<str:filename>', view_pdf, name='labeling_pdf'),
    path('labeling/entity/report/', views.report, name='labeling_entity_report'),
    path('labeling/entity/test', views.report_panel, name='test')
]   