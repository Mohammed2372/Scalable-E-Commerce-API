from rest_framework.serializers import ModelSerializer

from .models import Cart, CartItem


class CartItemSerializer(ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["id", "product_id", "quantity"]


class CartSerializer(ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "user_id", "created_at", "items"]
