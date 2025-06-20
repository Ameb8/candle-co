from rest_framework import serializers
from .models import Product, ProductImages
import cloudinary.uploader

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        image_file = validated_data.pop('image', None)
        product = Product.objects.create(**validated_data)

        if image_file:
            # Upload to Cloudinary with the preset
            upload_result = cloudinary.uploader.upload(
                image_file,
                upload_preset="django_secure_upload",  # Your preset name
                resource_type="image"
            )
            # Save the Cloudinary URL to the model
            product.image = upload_result['secure_url']
            product.save()

        return product

class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = '__all__'