from django.urls import path
from .views import *

urlpatterns = [
    path('', DeliveryDashboard, name='DeliveryDashboard'),
    path('login/', DeliveryLogin, name='DeliveryPartnerLogin'),
    path('logout/', DeliveryLogout, name='DeliveryPartnerLogout'),
    path('verfyOtp/', VerifyOtp, name='VerifyOtp'),
    path('order/<int:order_id>/status', UpdateDeliveryStatus, name='UpdateDeliveryStatus'),
    path('update-location/', update_delivery_location, name='update_delivery_location'),
]