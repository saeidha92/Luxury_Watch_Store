from rest_framework import serializers

from .models import (
    Brand,
    Category,
    Comment,
    Customer,
    Product,
    ProductColor,
    ProductImage,
    WishList,
)


class BrandMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name"]


class CategoryMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image"]


class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = ["id", "color", "hex_code"]


class CommentSerializer(serializers.ModelSerializer):
    customer_username = serializers.CharField(
        source="customer.user.username", read_only=True
    )

    class Meta:
        model = Comment
        fields = ["id", "customer_username", "body", "created_at"]


# ---------------------------------------------------------------------------
# 1) /api/products/
# ---------------------------------------------------------------------------


class ProductListSerializer(serializers.ModelSerializer):
    brand = BrandMiniSerializer(read_only=True)
    category = CategoryMiniSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "slug",
            "price",
            "brand",
            "category",
            "is_available",
            "stash",
        ]


# ---------------------------------------------------------------------------
# 2) /api/products/{slug}/
# ---------------------------------------------------------------------------


class ProductDetailSerializer(serializers.ModelSerializer):
    brand = BrandMiniSerializer(read_only=True)
    category = CategoryMiniSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    colors = ProductColorSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "slug",
            "brand",
            "category",
            "price",
            "is_discount",
            "is_available",
            "is_special",
            "gender",
            "origin",
            "strap_matterial",
            "usage",
            "design",
            "engine",
            "main_image",
            "features",
            "is_luxury",
            "description",
            "meta_title",
            "meta_description",
            "stash",
            "click_count",
            "created_at",
            "updated_at",
            "images",
            "colors",
            "comments",
        ]


# ---------------------------------------------------------------------------
# 3) /api/luxury-special/
# ---------------------------------------------------------------------------


class LuxurySpecialSerializer(serializers.ModelSerializer):
    avg_luxury_price = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True
    )

    class Meta:
        model = Product
        fields = [
            "title",
            "price",
            "gender",
            "strap_matterial",
            "engine",
            "avg_luxury_price",
        ]


# ---------------------------------------------------------------------------
# 4) /api/me/wishlist/
# ---------------------------------------------------------------------------


class ProductForWishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["title", "slug", "price", "stash", "main_image"]


class CustomerForWishlistSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Customer
        fields = ["username", "email", "phone_number"]


class WishListSerializer(serializers.ModelSerializer):
    product = ProductForWishlistSerializer(read_only=True)
    customer = CustomerForWishlistSerializer(read_only=True)

    class Meta:
        model = WishList
        fields = ["product", "customer"]
