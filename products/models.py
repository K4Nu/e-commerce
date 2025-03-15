import os.path

from django.db import models
from django.db.models import Q

class CategoryManager(models.Manager):
    def roots(self):
        return self.filter(parent__isnull=True)

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        null=True,
        blank=True,
        db_index=True  # Django creates an index for FKs by default, but we can specify this explicitly.
    )
    objects = CategoryManager()

    def __str__(self):
        names = []
        current = self
        while current:
            names.append(current.name)
            current = current.parent
        return '>'.join(reversed(names))

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=('parent_id',), name='category_parent_idx'),
        ]

class Size(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name='sizes')

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=('category_id', 'name'), name='category_size'),
        ]

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')
    size = models.ForeignKey('Size', on_delete=models.CASCADE, related_name='products')
    quantity = models.PositiveIntegerField()
    image= models.ForeignKey('Images', on_delete=models.CASCADE, related_name='products')
    @property
    def is_stock(self):
        return self.quantity > 0

    def __str__(self):
        categories = []
        parent = self.category
        while parent:
            categories.append(parent.name)
            parent = parent.parent
        category_path = " > ".join(reversed(categories))
        return f"{category_path} - {self.name}" if category_path else self.name

    class Meta:
        indexes = [
            models.Index(fields=('category_id', 'name'), name='product_name'),
            models.Index(fields=('quantity',), name='product_in_stock', condition=Q(quantity__gt=0)),
        ]


def product_image_upload_path(instance, filename):
    return os.path.join('products', str(instance.product.id), filename)

class Images(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=product_image_upload_path)
