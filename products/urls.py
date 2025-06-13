from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, max_price_available_product, ProductImagesViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'product-details', ProductImagesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('max-price/', max_price_available_product, name='max-price'),
]
