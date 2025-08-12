from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CustomDesign(models.Model):
    SIZE_CHOICES = [
        ('A5', 'A5 (14.8 × 21 cm)'),
        ('A4', 'A4 (21 × 29.7 cm)'),
        ('A3', 'A3 (29.7 × 42 cm)'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    framed = models.BooleanField(default=False)
    design_file = models.FileField(upload_to='custom_designs/')
    phone_number = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.size} - {'Framed' if self.framed else 'Unframed'}"
    
    def add_to_cart(self):
        from cart.models import CartItem
        CartItem.objects.create(
            user=self.user,
            product_name=f"Custom Design ({self.size}, {'Framed' if self.framed else 'Unframed'})",
            quantity=1,
            price=self.calculate_price(),
            custom_design=self
        )
        
    def calculate_price(self):
        base_prices = {'A3': 25, 'A4': 20, 'A5': 15}  
        price = base_prices.get(self.size, 15)
        if self.framed:
            price += 50  
        return price

