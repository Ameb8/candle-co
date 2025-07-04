from django.db import models
from cloudinary.models import CloudinaryField

class Product(models.Model):
    # Product info
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=60, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    image = CloudinaryField('image', folder='products', null=True, blank=True)
    description = models.TextField(null=True)

    # Inventory data
    amount = models.PositiveIntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Weight
    weight_value = models.DecimalField(max_digits=6, decimal_places=2)  # e.g., 1.25
    weight_unit = models.CharField(max_length=2, choices=[('lb', 'Pounds'), ('oz', 'Ounces'), ('kg', 'Kilograms'), ('g', 'Grams')])

    # Dimensions
    length = models.DecimalField(max_digits=6, decimal_places=2)  # e.g., 4.00
    width = models.DecimalField(max_digits=6, decimal_places=2)
    height = models.DecimalField(max_digits=6, decimal_places=2)
    distance_unit = models.CharField(max_length=2, choices=[('in', 'Inches'), ('cm', 'Centimeters')])

    def __str__(self):
        return self.name

class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"Image for {self.product.name}"

