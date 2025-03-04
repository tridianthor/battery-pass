from django.urls import path

from . import views

urlpatterns = [
    path('cfperlifecyclese-autocomplete/', views.CFPerLifecycleSEAutoComplete.as_view(), name='cfperlifecyclese-autocomplete'),
]