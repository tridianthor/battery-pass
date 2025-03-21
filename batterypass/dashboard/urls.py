from django.urls import path
from django.views.generic.base import RedirectView

from utils.pdf import view_pdf

from . import views

urlpatterns = [
    path('batteries/', views.batteries, name='batteries'),
    path('summary/', views.summary, name='summary'),
    path('summary/<int:pk>/', views.summary, name='summary_pk'),
    path('summary/<str:code>/', views.summary, name='summary_code'),
    path('detail/', views.detail, name='detail'),
    path('detail/<int:pk>/', views.detail, name='detail_pk'),
    path('detail/<str:code>/', views.detail, name='detail_code'),
    path('', RedirectView.as_view(url='dashboard/'), name='root-redirect'),
    path('pdf<path:folder>/<str:filename>', view_pdf, name='view_pdf'),    
    path('pdf/<str:filename>', view_pdf, name='view_pdf'),    
]
