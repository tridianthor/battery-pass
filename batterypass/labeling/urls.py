from django.urls import path

from utils.pdf import view_pdf

from . import views
from .views import LabelingEntityAutoComplete

urlpatterns = [
    path('label/', views.labeling, name='labels'),
    path('label/delete/<int:pk>', views.delete_labeling, name='delete_label'),
    path('labels/', views.labeling_entity, name='label_entity'),
    path('labels/delete/<int:pk>', views.delete_labeling_entity, name='delete_label_entity'),
    path('label/form/', views.insert_labeling, name='insert_label'),
    path('label/form/<int:pk>', views.update_labeling, name='update_label'),
    path('labels/form/', views.insert_labeling_entity, name='insert_label_entity'),
    path('labels/form/<int:pk>', views.update_labeling_entity, name='update_label_entity'),
    path('labels-autocomplete/', LabelingEntityAutoComplete.as_view(), name='labels_autocomplete'), 
    path('label/pdf/<path:folder>/<str:filename>', view_pdf, name='labeling_pdf'),
    path('label/entity/report/', views.report, name='labeling_entity_report'),
    path('label/entity/test', views.report_panel, name='test')
]   