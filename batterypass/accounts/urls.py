from django.urls import path

from . import views

urlpatterns = [
    path('accounts/', views.accounts,name='accounts'),
    path('accounts/form/' , views.insert_account,name='insert_account'),
    path('accounts/form/<int:pk>', views.update_account,name='update_account'),
    path('accounts/delete/<int:pk>', views.delete_account,name='delete_account'),
    path('accounts/change-password/<int:pk>', views.change_password,name='change_password'),
    path('accounts/login/', views.auth, name='login'),
    path('accounts/logout/', views.deauth, name='logout'),
]
