from django.urls import path

from utils.pdf import view_pdf

from . import views

urlpatterns = [
    path('duediligence/', views.duediligence, name='duediligence'),
    path('duediligence/form/', views.insert_duediligence, name='duediligence_form'),
    path('duediligence/form/<int:pk>', views.update_duediligence, name='duediligence_form'),
    path('duediligence/delete/<int:pk>', views.delete, name='delete'),
    path('duediligence/pdf/<path:folder>/<str:filename>', view_pdf, name='duediligence_pdf'),
]