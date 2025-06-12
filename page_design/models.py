from django.db import models

class PageDesign(models.Model):
    about_us = models.CharField(max_length=100)
    banner_image = models.ImageField(upload_to='design/', null=True, blank=True)
    contact_num = models.CharField(max_length=20)
    contact_mail = models.CharField(max_length=60)
