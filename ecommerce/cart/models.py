from django.db import models
from django.conf import settings
from products.models import Product

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    SHIPPING_THRESHOLD = 500
    SHIPPING_COST = 50

    def __str__(self):
        return f"Cart {self.id}"

    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_shipping_cost(self):
        total = self.get_total_price()
        return 0 if total >= self.SHIPPING_THRESHOLD else self.SHIPPING_COST

    def is_free_shipping(self):
        return self.get_total_price() >= self.SHIPPING_THRESHOLD

    def get_total_price_with_shipping(self):
        return self.get_total_price() + self.get_shipping_cost()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_cost(self):
        return self.product.price * self.quantity
