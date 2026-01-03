from django.db import models
from django.db.models import Model


# Create your models here.
class Cart(Model):
    user_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Cart for User {self.user_id}"


class CartItem(Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product_id = models.IntegerField()
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("cart", "product_id")

    def __str__(self) -> str:
        return f"Product {self.product_id} x ({self.quantity}) in Cart {self.cart.id}"
