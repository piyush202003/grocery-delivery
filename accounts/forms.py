from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "phone",
            "avatar",
            "is_admin",
            "is_delivery_partner",
            "is_active",
            "is_staff",
            "is_superuser",
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "phone",
            "avatar",
            "is_admin",
            "is_delivery_partner",
            "is_active",
            "is_staff",
            "is_superuser",
        )