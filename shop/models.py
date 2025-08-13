from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    FRAME_CHOICES = [
        ('framed', 'Framed'),
        ('frameless', 'Frameless'),
    ]
    
    SIZE_CHOICES = [
        ('A5', 'A5 (14.8 × 21 cm)'),
        ('A4', 'A4 (21 × 29.7 cm)'),
        ('A3', 'A3 (29.7 × 42 cm)'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    framed = models.BooleanField(default=False)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, default='A4')
    
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True)
    
    views_count = models.PositiveIntegerField(default=0)
    sales_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.get_size_display()} - {'Framed' if self.framed else 'Frameless'}"
    
    def get_final_price(self):
        base_prices = {
            'A5': 25,
            'A4': 30,
            'A3': 35,
        }
        
        price = base_prices.get(self.size, 30)
        
        if self.framed:
            price += 70
        
        return price

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class CustomDesign(models.Model):
    SIZE_CHOICES = [
        ('A5', 'A5 (14.8 × 21 cm)'),
        ('A4', 'A4 (21 × 29.7 cm)'),
        ('A3', 'A3 (29.7 × 42 cm)'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    framed = models.BooleanField(default=False)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, default='A4')
    design_file = models.FileField(upload_to='custom_designs/')
    phone_number = models.CharField(max_length=20)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.get_size_display()} - {'Framed' if self.framed else 'Frameless'}"
    
    def add_to_cart(self):
        from cart.models import CartItem
        CartItem.objects.create(
            user=self.user,
            product_name=f"Custom Design ({self.get_size_display()}, {'Framed' if self.framed else 'Frameless'})",
            quantity=1,
            price=self.calculate_price(),
            custom_design=self
        )
        
    def calculate_price(self):
        base_prices = {
            'A5': 25,
            'A4': 30,
            'A3': 35,
        }
        
        price = base_prices.get(self.size, 30)
        
        if self.framed:
            price += 70
        
        return price


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['product', 'user']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.rating} stars"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=20, unique=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()
    phone_number = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.order_number} - {self.user.username}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"RHINO{self.id:06d}"
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    custom_design = models.ForeignKey(CustomDesign, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.product_name} - {self.order.order_number}"


class PromoCode(models.Model):
    DISCOUNT_TYPES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ]
    
    code = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=200)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPES, default='percentage')
    discount_value = models.DecimalField(max_digits=8, decimal_places=2)
    min_order_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    max_uses = models.PositiveIntegerField(default=0)  # 0 means unlimited
    used_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.code} - {self.description}"
    
    def is_valid(self):
        from django.utils import timezone
        now = timezone.now()
        return (
            self.is_active and
            now >= self.valid_from and
            now <= self.valid_until and
            (self.max_uses == 0 or self.used_count < self.max_uses)
        )
    
    def calculate_discount(self, order_total):
        if order_total < self.min_order_amount:
            return 0
        
        if self.discount_type == 'percentage':
            discount = (order_total * self.discount_value) / 100
        else:  # fixed amount
            discount = min(self.discount_value, order_total)
        
        return discount
    
    def use_code(self):
        if self.is_valid():
            self.used_count += 1
            self.save()
            return True
        return False

