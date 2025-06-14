from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Max, F
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_POST
# from .permissions import IsAdminOrReadOnly
from .models import PageDesign, DesignImage, ImageList, ImageInList
from .serializers import (
    PageDesignSerializer,
    ImageInListSerializer,
    ImageInListCreateSerializer
)



class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow GET for anyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow POST/PATCH only for staff
        return request.user and request.user.is_authenticated and request.user.is_staff


class SingletonPageDesignViewSet(viewsets.ViewSet):
    permission_classes = [IsStaffOrReadOnly]

    def get_object(self):
        obj = PageDesign.objects.first()
        if not obj:
            raise PageDesign.DoesNotExist("No PageDesign object exists.")
        return obj

    def list(self, request):
        obj = PageDesign.objects.first()
        if not obj:
            return Response({'detail': 'No design yet.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PageDesignSerializer(obj)
        return Response(serializer.data)

    def create(self, request):
        if PageDesign.objects.exists():
            return Response({'detail': 'PageDesign already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PageDesignSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        # Ignore the PK, always update the singleton
        try:
            obj = self.get_object()
        except PageDesign.DoesNotExist:
            return Response({'detail': 'No PageDesign exists.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PageDesignSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageInListViewSet(viewsets.ModelViewSet):
    queryset = ImageInList.objects.select_related('image', 'image_list').all()
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ImageInListCreateSerializer
        return ImageInListSerializer

    def get_queryset(self):
        # Optional filtering by list
        list_name = self.request.query_params.get('list_name')
        if list_name:
            return self.queryset.filter(image_list__name=list_name)
        return self.queryset.order_by('position')

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def reorder(self, request):
        ordered_ids = request.data.get('ordered_ids')  # [3, 5, 1, 8]
        if not ordered_ids:
            return Response({'error': 'No ordered_ids provided'}, status=400)

        for i, id in enumerate(ordered_ids):
            ImageInList.objects.filter(id=id).update(position=i + 1)

        return Response({'status': 'reordered'})
