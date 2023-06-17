from django.urls import path
from . import views

app_name = 'inventory'
urlpatterns = [
    path('inventory_list', views.inventory_list, name='inventory_list'),
    path('per_product/<int:pk>', views.per_product, name='per_product'),
    path('add_product/', views.add_products, name='add_product'),
    path('', views.dashboard, name='dashboard'),
]