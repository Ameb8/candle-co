from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=60, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # Stripe recommends Decimal for accurate pricing
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    description = models.TextField(null=True)
    amount = models.PositiveIntegerField(null=True)  # number of items or inventory count
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
