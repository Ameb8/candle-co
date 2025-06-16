from rest_framework import serializers
from .models import Order, OrderItem, Address
from products.models import Product

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'full_name', 'street_address', 'apartment_address',
            'city', 'state', 'postal_code', 'country', 'phone_number'
        ]

class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta:
        model = OrderItem
        fields = ['product_id', 'quantity']

class CreateOrderSerializer(serializers.Serializer):
    email = serializers.EmailField()
    items = OrderItemSerializer(many=True)
    shipping_address = AddressSerializer()

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Order must contain at least one item.")
        return value

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
