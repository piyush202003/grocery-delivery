from django.urls import path
from .views import *

urlpatterns = [
    path("", Home, name = "Home"),

    path("products/", Products, name="Products"),
    path("products/<int:pdid>/", ProductPage, name = "ProductPage"),
    path("search/", SearchResults, name="SearchResults"),
    path("deals/", FlashDeals, name = "FlashDeals"),
    
    path("checkout/", Checkout, name="Checkout"),

    path("orders/", MyOrders, name="MyOrders"),
    path("orders/<int:odid>/", OrderTracking, name = "OrderTracking"),
    path('api/order/<str:odid>/update-location/', update_driver_location, name='update_driver_location'),

    path("addresses/", Addresses, name = "Addresses"),
    path('addresses/<int:id>/edit', Addresses, name='AddressEdit'),
    path('addresses/<str:addid>/delete', AddressDelete, name='AddressDelete'),

    path("cart/add/<str:product_id>/", add_to_cart, name="AddToCart"),
    path("cart/remove/<str:product_id>/", remove_from_cart, name="RemoveFromCart"),
    path("cart/update/<str:product_id>/", update_cart, name="UpdateCart"),
    path("cart/clear/", clear_cart, name="ClearCart"),
    
]