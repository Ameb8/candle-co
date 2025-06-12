from rest_framework import viewsets
from django.shortcuts import render
from .permissions import IsAdminOrReadOnly
from .permissions import IsAdminOrReadOnly

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]