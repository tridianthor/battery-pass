from django.urls import path

from . import views

urlpatterns = [
    path('products/', views.products, name='products'),
    path('products/delete/<int:pk>', views.delete_products, name='delete_product'),
    path('products/form/', views.insert_product, name='insert_product'),
    path('products/form/<int:pk>', views.update_product, name='update_product')
]