from django.urls import path
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/<int:pk>/', views.dashboard, name='dashboard_pk'),
    path('dashboard/<str:code>/', views.dashboard, name='dashboard_code'),
    path('', RedirectView.as_view(url='dashboard/'), name='root-redirect'),    
]
