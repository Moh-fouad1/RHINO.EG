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


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    promo_code = models.ForeignKey('shop.PromoCode', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cart for {self.user.username}"
    
    def get_items(self):
        return CartItem.objects.filter(user=self.user)
    
    def get_subtotal(self):
        items = self.get_items()
        return sum(item.total_price() for item in items)
    
    def get_discount(self):
        if not self.promo_code or not self.promo_code.is_valid():
            return 0
        return self.promo_code.calculate_discount(self.get_subtotal())
    
    def get_total(self):
        subtotal = self.get_subtotal()
        discount = self.get_discount()
        return max(0, subtotal - discount)
    
    def get_item_count(self):
        items = self.get_items()
        return sum(item.quantity for item in items)
