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
        fields = ['id', 'image', 'position']

class ImageInListCreateSerializer(serializers.Serializer):
    image = serializers.ImageField()
    list_name = serializers.ChoiceField(choices=ImageList.LIST_CHOICES, write_only=True)  # ✅ write_only

    def create(self, validated_data):
        list_name = validated_data.pop('list_name')
        image_file = validated_data.pop('image')

        image_list, _ = ImageList.objects.get_or_create(name=list_name)
        design_image = DesignImage.objects.create(image=image_file)

        max_position = (
            ImageInList.objects.filter(image_list=image_list)
            .aggregate(Max('position'))['position__max'] or 0
        )

        return ImageInList.objects.create(
            image=design_image,
            image_list=image_list,
            position=max_position + 1
        )
