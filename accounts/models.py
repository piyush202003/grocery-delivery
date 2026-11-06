from django.db import models
from django.contrib.auth.models import AbstractUser
from .services.geocoding import geocode_address

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_delivery_partner = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    label = models.CharField(max_length=50)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)
    lat = models.DecimalField( max_digits=10, decimal_places=7)
    lng = models.DecimalField( max_digits=10, decimal_places=7) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} => {self.label}'