from django.urls import path
from .views import *

urlpatterns = [
    path('', AdminDashboard, name='AdminDashboard'),
    path('products/', AdminProducts, name='AdminProducts'),
    path('products/new/', AdminProductForm, name='AdminProductForm'),
    path('products/<int:id>/edit/', AdminProductForm, name='AdminProductFormEdit'),
    path('products/<int:id>/out_of_stock/', AdminProductOutOfStock, name='AdminProductOutOfStock'),
    path('orders/', AdminOrders, name='AdminOrders'),
    path('delivery-partners/', AdminDeliveryPartners, name='AdminDeliveryPartners'),
    path('logout/', AdminLogout, name='AdminLogout'),    
]