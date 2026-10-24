from decimal import Decimal
import secrets

from django.db import models
from accounts.models import Address
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Category(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="categories/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='ProductCategory')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image = models.ImageField(upload_to="products/")
    unit = models.CharField(max_length=30, default='piece')
    stock = models.PositiveIntegerField(default=0)
    is_organic = models.BooleanField(default=False)
    rating = models.FloatField(default=0)
    review_count = models.PositiveIntegerField(default=0)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):

        if self.original_price is not None:
            discount_amount = (
                self.original_price * Decimal(self.discount) / Decimal(100)
            )
            self.price = self.original_price - round(discount_amount, 2)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveIntegerField(default=1)

class DeliveryPartner(models.Model):
    VEHICLE_TYPES = [
        ("bike", "Bike"),
        ("scooter", "Scooter"),
        ("car", "Car"),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="delivery_partner")
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES, default='bike')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.username

class Order(models.Model):
    STATUS_CHOICES = (
        ("Placed", "Placed"),
        ("Confirmed", "Confirmed"),
        ('Assigned', 'Assigned'),
        ("Packed", "Packed"),
        ("Out for Delivery", "Out for Delivery"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    )

    PAYMENT_METHODS = (
        ("card", "Card"),
        ("cash", "Cash"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="order")
    shipping_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="order")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='card')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Placed')
    delivery_partner = models.ForeignKey(DeliveryPartner, on_delete=models.SET_NULL, null=True, blank=True, related_name="order")
    delivery_otp = models.CharField(max_length=6, blank=True, default='')
    live_location = models.JSONField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.status == 'Out for Delivery':
            otp = secrets.randbelow(900000) +100000
            self.delivery_otp = str(otp)
        elif self.status not in ['Out for Delivery', 'Delivered']:
            self.delivery_otp = ''

        super().save(*args, **kwargs)
              
    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="OrderItemProduct")
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class OrderStatus(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="history")
    status = models.CharField(max_length=30)
    timestamp = models.DateTimeField(auto_now=True)
    note = models.TextField(blank=True, null=True)