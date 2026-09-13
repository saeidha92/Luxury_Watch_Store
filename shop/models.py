from django.db import models
from django.utils.text import slugify
from django.conf import settings

# Abstract base classes


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class SluggedMixinModel(models.Model):
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    class Meta:
        abstract = True

    def generate_unique_slug(self, source_field_value):
        base_slug = slugify(source_field_value, allow_unicode=True)
        slug = base_slug
        ModelClass = self.__class__
        counter = 1
        while ModelClass.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug


# Brand ------------------


class Brand(BaseModel):
    name = models.CharField(max_length=255)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# category ------------------


class Category(BaseModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        # auto generate slug from title if not provided manually
        if not self.slug:
            base_slug = slugify(self.title, allow_unicode=True)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# Product ------------------


class Product(BaseModel, SluggedMixinModel):
    # ---- choice field options (watch-related product, adjust freely) ----
    class Gender(models.TextChoices):
        MEN = "men", "Men"
        WOMEN = "women", "Women"
        UNISEX = "unisex", "Unisex"

    class Origin(models.TextChoices):
        DOMESTIC = "domestic", "Domestic"
        IMPORTED = "imported", "Imported"

    class StrapMaterial(models.TextChoices):
        LEATHER = "leather", "Leather"
        METAL = "metal", "Metal"
        RUBBER = "rubber", "Rubber"
        FABRIC = "fabric", "Fabric"

    class Usage(models.TextChoices):
        SPORT = "sport", "Sport"
        CASUAL = "casual", "Casual"
        FORMAL = "formal", "Formal"

    class Design(models.TextChoices):
        CLASSIC = "classic", "Classic"
        MODERN = "modern", "Modern"
        VINTAGE = "vintage", "Vintage"

    class Engine(models.TextChoices):
        AUTOMATIC = "automatic", "Automatic"
        QUARTZ = "quartz", "Quartz"
        MECHANICAL = "mechanical", "Mechanical"

    title = models.CharField(max_length=255)

    # ---- foreign keys ----
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )

    # ---- price & stock fields ----
    price = models.DecimalField(max_digits=12, decimal_places=2)
    is_discount = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    is_special = models.BooleanField(default=False)

    # ---- choice fields ----
    gender = models.CharField(max_length=20, choices=Gender.choices, blank=True)
    origin = models.CharField(max_length=20, choices=Origin.choices, blank=True)
    strap_matterial = models.CharField(
        max_length=20, choices=StrapMaterial.choices, blank=True
    )  # keeping the exact (misspelled) field name used in the exercise sheet
    usage = models.CharField(max_length=20, choices=Usage.choices, blank=True)
    design = models.CharField(max_length=20, choices=Design.choices, blank=True)
    engine = models.CharField(max_length=20, choices=Engine.choices, blank=True)

    # ---- other fields ----
    main_image = models.ImageField(upload_to="products/main/")
    features = models.JSONField(default=dict, blank=True)
    is_luxury = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    stash = models.PositiveIntegerField(default=0)  # inventory / stock count
    click_count = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ProductImage(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="products/gallery/")

    def __str__(self):
        return f"Image for {self.product.title}"


class ProductColor(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="colors"
    )
    color = models.CharField(max_length=100)
    hex_code = models.CharField(max_length=7)  # example: "#FFFFFF"

    def __str__(self):
        return f"{self.color} ({self.hex_code}) - {self.product.title}"


# wishlist --------------------------------------------


class WishList(BaseModel):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="wishlist_items"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="wishlisted_by"
    )

    class Meta:
        # required feature: a customer can add a specific product only once
        unique_together = ("product", "customer")

    def __str__(self):
        return f"{self.customer} -> {self.product}"


# ----------------------------------------------------------


# customer -------------------------------------------------


class Customer(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="customer"
    )
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username


# -------------------------------------------------------------

# comments ----------------------------------------------------


class Comment(BaseModel):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="comments"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="comments"
    )
    body = models.TextField()

    def __str__(self):
        return f"Comment by {self.customer} on {self.product}"
