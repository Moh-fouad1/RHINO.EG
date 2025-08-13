from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Category, Product, CustomDesign, Review, Order, OrderItem, PromoCode

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'product_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']
    ordering = ['name']

    def product_count(self, obj):
        return obj.product_set.count()
    product_count.short_description = 'Products'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'size', 'framed', 'price_display', 'in_stock', 'featured', 'is_active', 'views_count']
    list_filter = ['category', 'size', 'framed', 'in_stock', 'featured', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'category__name']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['in_stock', 'featured', 'is_active']
    ordering = ['-created_at']
    readonly_fields = ['views_count', 'sales_count', 'rating']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'category', 'image')
        }),
        ('Pricing & Options', {
            'fields': ('base_price', 'size', 'framed')
        }),
        ('Status & Statistics', {
            'fields': ('in_stock', 'featured', 'is_active', 'views_count', 'sales_count', 'rating')
        }),
    )

    def price_display(self, obj):
        return f"{obj.get_final_price()} LE"
    price_display.short_description = 'Price'

@admin.register(CustomDesign)
class CustomDesignAdmin(admin.ModelAdmin):
    list_display = ['user', 'size', 'framed', 'price_display', 'status', 'phone_number', 'created_at']
    list_filter = ['size', 'framed', 'status', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone_number', 'notes']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['status']
    ordering = ['-created_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'phone_number')
        }),
        ('Design Details', {
            'fields': ('size', 'framed', 'design_file', 'notes')
        }),
        ('Status & Timestamps', {
            'fields': ('status', 'created_at', 'updated_at')
        }),
    )

    def price_display(self, obj):
        return f"{obj.calculate_price()} LE"
    price_display.short_description = 'Price'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'is_approved', 'created_at']
    list_filter = ['rating', 'is_approved', 'created_at']
    search_fields = ['user__username', 'product__name', 'comment']
    readonly_fields = ['created_at']
    list_editable = ['is_approved']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Review Information', {
            'fields': ('user', 'product', 'rating', 'comment')
        }),
        ('Moderation', {
            'fields': ('is_approved', 'created_at')
        }),
    )

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'total_amount_display', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order_number', 'user__username', 'user__email', 'phone_number']
    readonly_fields = ['order_number', 'total_amount', 'created_at', 'updated_at']
    list_editable = ['status']
    ordering = ['-created_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'total_amount')
        }),
        ('Shipping Information', {
            'fields': ('shipping_address', 'phone_number')
        }),
        ('Status & Timestamps', {
            'fields': ('status', 'created_at', 'updated_at')
        }),
    )

    def total_amount_display(self, obj):
        return f"{obj.total_amount} LE"
    total_amount_display.short_description = 'Total Amount'

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'description', 'discount_type', 'discount_value_display', 'min_order_amount', 'is_active', 'valid_until', 'usage_count']
    list_filter = ['discount_type', 'is_active', 'valid_from', 'valid_until']
    search_fields = ['code', 'description']
    readonly_fields = ['used_count', 'created_at']
    list_editable = ['is_active']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Code Information', {
            'fields': ('code', 'description')
        }),
        ('Discount Settings', {
            'fields': ('discount_type', 'discount_value', 'min_order_amount')
        }),
        ('Usage Limits', {
            'fields': ('max_uses', 'used_count')
        }),
        ('Validity', {
            'fields': ('is_active', 'valid_from', 'valid_until')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )

    def discount_value_display(self, obj):
        if obj.discount_type == 'percentage':
            return f"{obj.discount_value}%"
        else:
            return f"${obj.discount_value}"
    discount_value_display.short_description = 'Discount'

    def usage_count(self, obj):
        if obj.max_uses == 0:
            return f"{obj.used_count} / ∞"
        else:
            return f"{obj.used_count} / {obj.max_uses}"
    usage_count.short_description = 'Usage'

admin.site.site_header = "RHINO.EG Administration"
admin.site.site_title = "RHINO.EG Admin"
admin.site.index_title = "Welcome to RHINO.EG Administration"
