from django.contrib import admin

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


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductColorInline(admin.TabularInline):
    model = ProductColor
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "brand",
        "category",
        "price",
        "is_available",
        "stash",
        "click_count",
    )
    list_filter = ("is_available", "is_special", "is_luxury", "gender")
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProductImageInline, ProductColorInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Brand)
admin.site.register(ProductImage)
admin.site.register(ProductColor)
admin.site.register(Customer)
admin.site.register(WishList)
admin.site.register(Comment)
