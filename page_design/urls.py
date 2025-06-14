from django.urls import path
from . import views

urlpatterns = [
    path('add-img', views.add_image, name='add_image'),
    path('move-img', views.move_image, name='move_image'),
    path('get-img', views.get_images, name='get_images'),
    path('remove-img', views.remove_image, name='remove_image'),
]