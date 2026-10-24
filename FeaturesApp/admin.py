from django.contrib import admin
from matplotlib.pyplot import cla

from .models import CartItem, DeliveryPartner, Order, OrderItem, OrderStatus, Product, Category

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'name', 'image', 'created_at', 'updated_at', )
    search_fields = ('slug', 'name', )
    ordering = ('-updated_at', )
    readonly_fields = ('created_at', 'updated_at', )

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'name', 'description', 'price', 'original_price', 'unit', 'stock', 'is_organic', 'rating', 'review_count', 'discount', 'created_at', 'updated_at')
    list_filter = ('category','is_organic', 'created_at',)
    search_fields = ('name','description','category',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at','updated_at', 'price')
    fieldsets = (
        ('Product Info',{
            'fields':('category', 'name', 'image', 'description', 'is_organic',)
        }),
        ('Product Costing Info',{
            'fields':('price', 'original_price', 'discount',)
        }),
        ('Storage Info',{
            'fields':('unit', 'stock', )
        }),
        ('Review and Rating Info',{
            'fields':('rating', 'review_count')
        }),
        ("Timestamps", {
            "fields": ("created_at", 'updated_at', )
        }),
    )

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', )
    list_filter = ('user', 'product', )
    search_fields = ('user', 'product', )

@admin.register(DeliveryPartner)
class DeliveryPartnerAdmin(admin.ModelAdmin):
    list_display = ( 'user', 'vehicle_type', 'is_active', 'created_at', 'updated_at', )
    list_filter = ('vehicle_type', 'is_active', )
    search_fields = ( 'user', )
    ordering = ('-created_at', )
    readonly_fields = ('created_at', 'updated_at', )
    fieldsets = (
        ('Partner Info',{
            'fields': ( 'user', )
        }),
        ('Vehicle Info',{
            'fields' : ('vehicle_type', 'is_active', )
        }),
        ('Time Stamp',{
            'fields':('created_at', 'updated_at', )
        })
    )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'shipping_address', 'payment_method', 'subtotal', 'delivery_fee', 'tax', 'total', 'status', 'delivery_partner', 'delivery_otp', 'live_location', 'is_paid', 'created_at', 'updated_at', )
    list_filter = ('payment_method', 'status', 'is_paid', 'updated_at', )
    search_fields = ('shipping_address', 'user', 'delivery_partner', )
    ordering = ('-updated_at', )
    readonly_fields = ('updated_at', 'created_at', )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', )
    search_field = ('order', 'product', )

@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ('order', 'status', 'timestamp', 'note', )
    list_filter = ('status', )
    readonly_fields = ('timestamp', )