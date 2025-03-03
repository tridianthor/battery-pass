from django.urls import path
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', RedirectView.as_view(url='dashboard/'), name='root-redirect'),    
]
