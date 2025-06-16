from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'admin/orders', views.AdminOrderViewSet, basename='admin-orders')

urlpatterns = [
    path('create-order/', views.CreateOrderView.as_view(), name='create-order'),
    path('stripe/webhook/', views.stripe_webhook, name='stripe-webhook'),
]