from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField as SerializerPhoneNumberField
from .models import Order, OrderItem, Address, Shipment, PhoneAlert, EmailAlert
from products.models import Product
from products.serializers import ProductSerializer

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

class OrderItemDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = '__all__'

class PublicOrderItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='product.name')
    price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2)
    image = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['name', 'price', 'image', 'quantity']

    def get_image(self, obj):
        return obj.product.image.url if obj.product.image else None


class PublicShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = ['carrier', 'tracking_number', 'shipped_at', 'estimated_arrival', 'is_delivered', 'notes']


class PublicOrderSummarySerializer(serializers.ModelSerializer):
    items = PublicOrderItemSerializer(many=True, read_only=True)
    shipment = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'order_code', 'created_at', 'status', 'total_amount', 'items', 'shipment']

    def get_shipment(self, obj):
        shipment = obj.shipments.first()
        return PublicShipmentSerializer(shipment).data if shipment else None

class PhoneAlertSerializer(serializers.ModelSerializer):
    number = SerializerPhoneNumberField(region='US')

    class Meta:
        model = PhoneAlert
        fields = '__all__'

class EmailAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailAlert
        fields = ['email']

class ShippingRateRequestSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    to_name = serializers.CharField()
    to_street1 = serializers.CharField()
    to_city = serializers.CharField()
    to_state = serializers.CharField()
    to_zip = serializers.CharField()
    to_country = serializers.CharField()