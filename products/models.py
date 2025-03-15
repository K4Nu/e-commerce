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