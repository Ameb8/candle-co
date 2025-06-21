from django.db import models
from django.contrib.auth.models import User
import uuid

class Address(models.Model):
    full_name = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255)
    apartment_address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.full_name}, {self.street_address}, {self.city}"

class Order(models.Model):
    # User info
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    email=models.EmailField()

    # Shipping info
    order_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)

    # Stripe info
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Order status
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('fulfilled', 'Fulfilled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Order summary
    total_amount = models.IntegerField(help_text="In cents")

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class Shipment(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='shipments')
    carrier = models.CharField(max_length=100, blank=True)
    tracking_number = models.CharField(max_length=100, blank=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    estimated_arrival = models.DateField(null=True, blank=True)
    is_delivered = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Shipment for Order {self.order.order_code}"

