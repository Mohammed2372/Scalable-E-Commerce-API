from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Cart, CartItem
from .serializers import CartSerializer
from .services import ProductService


# Create your views here.
class CartViewSet(ViewSet):
    def list(self, request) -> Response:
        user_id = request.query_params.get("user_id")

        if not user_id:
            return Response(
                {"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        cart, created = Cart.objects.get_or_create(user_id=user_id)
        return Response(CartSerializer(cart).data)

    @action(detail=False, methods=["post"])
    def add_item(self, request) -> Response:
        user_id = request.data.get("user_id")
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        # validate input
        if not user_id or not product_id:
            return Response(
                {"error": "user_id and product_id are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # check if product exists in product service
        product_data = ProductService.check_product_exists(product_id=product_id)
        if not product_data:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # add to DB
        cart, _ = Cart.objects.get_or_create(user_id=user_id)

        item, created = CartItem.objects.get_or_create(cart=cart, product_id=product_id)
        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity

        item.save()

        return Response({"message": "Item added", "product": product_data["name"]})
