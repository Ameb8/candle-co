from django.db import models

class PageDesign(models.Model):
    about_us_title = models.CharField(max_length=50)
    about_us_body = models.CharField(max_length=500)
    contact_num = models.CharField(max_length=20)
    contact_mail = models.CharField(max_length=60)

class DesignImage(models.Model):
    image = models.ImageField(upload_to='design/', null=False, blank=False)

class ImageList(models.Model):
    LIST_CHOICES = [
        ('about', 'About'),
        ('contact', 'Contact'),
    ]
    name = models.CharField(max_length=20, choices=LIST_CHOICES, unique=True)

class ImageInList(models.Model):
    image = models.ForeignKey(DesignImage, on_delete=models.CASCADE)
    image_list = models.ForeignKey(ImageList, on_delete=models.CASCADE)
    position = models.PositiveIntegerField()

    class Meta:
        unique_together = ('image_list', 'position')
        ordering = ['position']

