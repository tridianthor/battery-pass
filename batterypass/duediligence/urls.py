from django.urls import path

from utils.pdf import view_pdf

from . import views

urlpatterns = [
    path('due_diligence/', views.duediligence, name='duediligences'),
    path('due_diligence/form/', views.insert_duediligence, name='insert_duediligence'),
    path('due_diligence/form/<int:pk>', views.update_duediligence, name='update_duediligence'),
    path('due_diligence/delete/<int:pk>', views.delete, name='delete_duedligence'),
    path('due_diligence/pdf/<path:folder>/<str:filename>', view_pdf, name='duediligence_pdf'),
]