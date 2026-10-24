from django.db import models
from django.contrib.auth.models import AbstractUser
from .services.geocoding import geocode_address

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
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
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.is_default:
            Address.objects.filter(
                user=self.user,
                is_default=True
            ).exclude(
                id=self.id
            ).update(is_default=False)

        if self.lat is None or self.lng is None:

            full_address = ( f"{self.address}, {self.city}, {self.state}, {self.zip}, India")

            lat, lng = geocode_address(full_address)

            if lat is not None and lng is not None:
                self.lat = lat
                self.lng = lng


        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} => {self.label}'