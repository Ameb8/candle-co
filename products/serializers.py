from rest_framework import serializers
from .models import Product, ProductImages
import cloudinary.uploader

class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()  # writable

    # override image field of output to just url
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = instance.image.url if instance.image else None
        return representation

    class Meta:
        model = Product
        fields = '__all__'


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = '__all__'