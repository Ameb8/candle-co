from django.urls import path
from . import views

urlpatterns = [
    path('orders/', views.orders_over_time, name='orders-over-time'),
]