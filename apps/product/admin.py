from django.contrib import admin

# Register your models here.
from product.models import Category, Product, ProductImage, OrderItem, Order
from product.models.banner import BannerDeco


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_active']
    list_display_links = ['name']


@admin.register(BannerDeco)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'photo', 'is_active']
    list_display_links = ['id', 'photo']


class ProductImageAdmin(admin.TabularInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_sale', 'price', 'quantity', 'is_banner']
    inlines = [ProductImageAdmin, ]
    list_display_links = ['name']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Set the number of inline forms to display


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone_number', 'mail', 'status')
    list_display_links = ('id', 'full_name', 'phone_number', 'mail', 'status')
    inlines = [OrderItemInline]  # Embed OrderItem inline in Order admin
    list_filter = ['status']
    search_fields = ('id', 'full_name',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'order_id',)
    list_display_links = ('order', 'product', 'quantity', 'order_id')
    list_filter = ['product__name']
    search_fields = ('id',)
