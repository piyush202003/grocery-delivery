from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Address
from .forms import CustomUserCreationForm, CustomUserChangeForm


@admin.register(User)
class UserAdmin(BaseUserAdmin):

    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm

    list_display = ( "email", "username", "first_name", "last_name", "is_admin", "is_delivery_partner", "is_staff", "is_active", )

    ordering = ("email",)
    readonly_fields = ( "last_login","date_joined",)
    fieldsets = (
        ( "Login information", { "fields": ( "email", "username", "password", ) }, ),
        ( "Personal information", { "fields": ( "first_name", "last_name", "phone", "avatar", ) },),
        ( "Permissions", { "fields": ( "is_staff", "is_superuser", "is_admin", "is_delivery_partner", )}, ),
        ( "Important dates", { "fields": ( "last_login", "date_joined", ) }),
    )

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'label', 'address', 'city', 'state', 'zip', 'is_default', 'lat', 'lng', 'created_at', 'updated_at', )
    search_fields = ('address', 'city', 'state', )
    readonly_fields = ('created_at', 'updated_at', )
    list_filter = ( 'label', )
    