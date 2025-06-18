from django.db.models import Max
from rest_framework import serializers
from .models import PageDesign, DesignImage, ImageList, ImageInList

class PageDesignSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageDesign
        fields = '__all__'

class DesignImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignImage
        fields = ['id', 'image']

class ImageInListSerializer(serializers.ModelSerializer):
    image = DesignImageSerializer()

    class Meta:
        model = ImageInList
        fields = ['id', 'image', 'image_list', 'order']

class ImageInListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageInList
        fields = ['id', 'image', 'image_list']

