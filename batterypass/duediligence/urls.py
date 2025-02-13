from django.urls import path

from . import views

url_patterns = [
    path('/duediligence', views.duediligence, name='duediligence'),
    path('/duediligence/forms', views.duediligence_form, name='duediligence_form'),
]