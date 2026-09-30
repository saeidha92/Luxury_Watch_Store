from django.db.models import Avg, F, Window
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, WishList
from .serializers import (
    LuxurySpecialSerializer,
    ProductDetailSerializer,
    ProductListSerializer,
    WishListSerializer,
)

# ---------------------------------------------------------------------------
# 1) GET /api/products/
# ---------------------------------------------------------------------------


class ProductListAPIView(APIView):
    """
    select_related() is used (not prefetch_related) because brand and
    category are *ForeignKey* fields (one-to-one from Product's point of
    view), so Django can fetch them with a single SQL JOIN in one query.
    """

    def get(self, request):
        products = Product.objects.select_related("brand", "category").all()
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)


# ---------------------------------------------------------------------------
# 2) GET /api/products/<slug>/
# ---------------------------------------------------------------------------


class ProductDetailAPIView(APIView):
    def get(self, request, slug):
        Product.objects.filter(slug=slug).update(click_count=F("click_count") + 1)

        product = get_object_or_404(
            Product.objects.select_related("brand", "category").prefetch_related(
                "images",
                "colors",
                "comments__customer__user",
            ),
            slug=slug,
        )
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)


# ---------------------------------------------------------------------------
# 3) GET /api/luxury-special/
# ---------------------------------------------------------------------------


class LuxurySpecialAPIView(APIView):
    def get(self, request):
        products = Product.objects.filter(
            is_special=True,
            is_luxury=True,
            is_available=True,
        ).annotate(
            avg_luxury_price=Window(expression=Avg("price")),
        )
        serializer = LuxurySpecialSerializer(products, many=True)
        return Response(serializer.data)


# ---------------------------------------------------------------------------
# 4) GET /api/me/wishlist/
# ---------------------------------------------------------------------------


class MyWishListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlist_items = WishList.objects.filter(
            customer__user=request.user
        ).select_related("product", "customer__user")
        serializer = WishListSerializer(wishlist_items, many=True)
        return Response(serializer.data)
