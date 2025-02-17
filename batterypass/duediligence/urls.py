from django.urls import path

from . import views

urlpatterns = [
    path('duediligence/', views.duediligence, name='duediligence'),
    path('duediligence/form/', views.duediligence_form, name='duediligence_form'),
    path('duediligence/form/<int:pk>', views.duediligence_form, name='duediligence_form'),
    path('duediligence/delete/<int:pk>', views.delete, name='delete'),
    path('duediligence/pdf/<path:folder>/<str:filename>', views.view_pdf, name='duediligence_pdf'),
]