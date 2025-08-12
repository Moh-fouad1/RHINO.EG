from django.db import models
from django.conf import settings

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE, null=True, blank=True)
    product_name = models.CharField(max_length=255, blank=True, null=True)
    custom_design = models.ForeignKey('shop.CustomDesign', on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.product:
            return f"{self.product.name} (x{self.quantity})"
        elif self.custom_design:
            return f"Custom Design ({self.custom_design.size})"
        return "Cart Item"
    
    def total_price(self):
        return self.price * self.quantity
