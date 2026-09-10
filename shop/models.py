from django.db import models
from django.utils.text import slugify

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

    
