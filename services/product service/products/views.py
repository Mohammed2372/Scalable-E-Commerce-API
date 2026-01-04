from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core.cache import cache

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


# Create your views here.
class CategoryViewSet(
    ReadOnlyModelViewSet
):  # ReadOnlyModelViewSet provides list and retrieve, blocks post and delete
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        cache_key = "product_list"

        # try to fetch from redis
        cached_data = cache.get(cache_key)
        if cached_data:
            print("🚀 Serving from Redis Cache", flush=True)
            return Response(cached_data)

        # if missed, fetch from database
        print("🐢 Serving from Database", flush=True)
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        # save to redis for next time
        cache.set(cache_key, data, timeout=60 * 15)

        return Response(data)
