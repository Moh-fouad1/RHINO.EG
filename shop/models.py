from django.db import models
from django.contrib.auth.models import User


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

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custom_designs')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    design_file = models.ImageField(upload_to='custom_designs/')
    size = models.CharField(max_length=2, choices=SIZE_CHOICES)
    phone_number = models.CharField(max_length=15)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"{self.title} by {self.user.username}"
