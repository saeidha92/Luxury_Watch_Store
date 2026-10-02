from django.urls import path

from .views import (
    LuxurySpecialAPIView,
    MyWishListAPIView,
    ProductDetailAPIView,
    ProductListAPIView,
)

urlpatterns = [
    path("products/", ProductListAPIView.as_view(), name="product-list"),
    path("products/<str:slug>/", ProductDetailAPIView.as_view(), name="product-detail"),
    path("luxury-special/", LuxurySpecialAPIView.as_view(), name="luxury-special"),
    path("me/wishlist/", MyWishListAPIView.as_view(), name="my-wishlist"),
]
