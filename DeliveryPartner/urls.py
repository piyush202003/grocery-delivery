from django.urls import path
from .views import *

urlpatterns = [
    path('', DeliveryDashboard, name='DeliveryDashboard'),
    path('login/', DeliveryLogin, name='DeliveryPartnerLogin'),
    path('logout/', DeliveryLogout, name='DeliveryPartnerLogout'),
    path('verfyOtp/', VerifyOtp, name='VerifyOtp'),
    path('delivery/order/<int:order_id>/status', UpdateDeliveryStatus, name='UpdateDeliveryStatus'),
    
]