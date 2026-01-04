from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Order, OrderItem
from .serializers import OrderSerializer
from .services import CartService, ProductService
from producer import publish_order_created


# Create your views here.
class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=False, methods=["post"])
    def checkout(self, request):
        user_id = request.data.get("user_id")

        if not user_id:
            return Response({"error": "User ID is required"}, status=400)

        # get items form cart service
        cart = CartService.get_cart(user_id=user_id)

        if not cart:
            return Response({"error": f"Can't get cart for user {user_id}"}, status=400)

        if not cart.get("items"):
            return Response({"error": "Cart is empty"}, status=400)

        # calculate total price and prepare order items
        total_price = 0
        order_items_to_create = []

        for item in cart["items"]:
            # get price form product service
            product = ProductService.get_product(product_id=item["product_id"])

            if not product:
                return Response(
                    {"error": f"Product {item['product_id']} not found"}, status=400
                )

            price = float(product["price"])
            total_price = price * item["quantity"]

            order_items_to_create.append(
                {
                    "product_id": item["product_id"],
                    "quantity": item["quantity"],
                    "price": price,
                }
            )

            # save order to db
            order = Order.objects.create(
                user_id=user_id,
                total_price=total_price,
                status="completed",
            )

            # save order items
            for item_data in order_items_to_create:
                OrderItem.objects.create(
                    order=order,
                    product_id=item_data["product_id"],
                    quantity=item_data["quantity"],
                    price=item_data["price"],
                )

            # clear the cart
            CartService.clear_cart(user_id=user_id)

            # async notification with RabbitMQ
            publish_order_created(
                {
                    "order_id": order.id,
                    "user_id": user_id,
                    "total_price": total_price,
                    "status": "completed",
                    "email": request.data.get("email", ""),
                }
            )

            return Response(
                {
                    "message": "Order placed successfully",
                    "order_id": order.id,
                    "total_price": total_price,
                },
                status=200,
            )
