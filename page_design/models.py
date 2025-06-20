from django.db import models
from ordered_model.models import OrderedModel
from cloudinary.models import CloudinaryField

class PageDesign(models.Model):
    about_us_title = models.CharField(max_length=50)
    about_us_body = models.CharField(max_length=500)
    contact_num = models.CharField(max_length=20)
    contact_mail = models.CharField(max_length=60)

class DesignImage(models.Model):
    image = CloudinaryField('image', folder='page-design', null=False, blank=False)

class ImageList(models.Model):
    LIST_CHOICES = [
        ('about', 'About'),
        ('contact', 'Contact'),
    ]
    name = models.CharField(max_length=20, choices=LIST_CHOICES, unique=True)

class ImageInList(OrderedModel):
    image = models.ForeignKey(DesignImage, on_delete=models.CASCADE)
    image_list = models.ForeignKey(ImageList, on_delete=models.CASCADE)

    class Meta:
        order_with_respect_to = 'image_list'
