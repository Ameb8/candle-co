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
        obj, created = PageDesign.objects.get_or_create(id=1, defaults={
            'about_us_title': '',
            'about_us_body': '',
            'contact_num': '',
            'contact_mail': ''
        })
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

    @action(detail=False, methods=["patch"])
    def update_text(self, request):
        obj = self.get_object()
        serializer = PageDesignSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ImageInListViewSet(viewsets.ModelViewSet):
    queryset = ImageInList.objects.select_related('image', 'image_list').all()
    # permission_classes = [permissions.IsAdminUser]

    def get_permissions(self):
        # Allow unauthenticated GET if querying for 'about' or 'contact'
        if self.action == 'list':
            list_name = self.request.query_params.get('list_name')
            if self.request.method == 'GET' and list_name in ['about', 'contact']:
                return [permissions.AllowAny()]
        # All other actions require admin
        return [permissions.IsAdminUser()]

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




'''
def add_image(request, list_name):
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)

    if request.method == 'POST' and request.FILES.get('image'):
        # Get or create the uploaded image
        uploaded_image = request.FILES['image']
        design_image = DesignImage.objects.create(image=uploaded_image)

        # Get the list (e.g. 'about', 'contact')
        image_list = get_object_or_404(ImageList, name=list_name)

        # Find the next available position in the list
        max_position = ImageInList.objects.filter(image_list=image_list).aggregate(
            max_pos=Max('position')
        )['max_pos'] or 0

        # Add the image to the list at the next position
        ImageInList.objects.create(
            image=design_image,
            image_list=image_list,
            position=max_position + 1
        )

        return JsonResponse({'status': 'success', 'image_id': design_image.id})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@require_POST
def move_image(request, list_name):
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)

    try:
        image_id = int(request.POST['image_id'])
        new_position = int(request.POST['new_position'])
    except (KeyError, ValueError):
        return JsonResponse({'status': 'error', 'message': 'Missing or invalid parameters'}, status=400)

    image_list = get_object_or_404(ImageList, name=list_name)
    image = get_object_or_404(DesignImage, id=image_id)

    try:
        image_entry = ImageInList.objects.get(image=image, image_list=image_list)
    except ImageInList.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Image not in list'}, status=404)

    old_position = image_entry.position

    if new_position == old_position:
        return JsonResponse({'status': 'success', 'message': 'No change needed'})

    # Shift positions of other images
    if new_position < old_position:
        # Moving up: shift down others in between
        ImageInList.objects.filter(
            image_list=image_list,
            position__gte=new_position,
            position__lt=old_position
        ).update(position=F('position') + 1)
    else:
        # Moving down: shift up others in between
        ImageInList.objects.filter(
            image_list=image_list,
            position__gt=old_position,
            position__lte=new_position
        ).update(position=F('position') - 1)

    # Update the moved image's position
    image_entry.position = new_position
    image_entry.save()

    return JsonResponse({'status': 'success', 'new_position': new_position})

def get_images(request, list_name):
    # Get the image list object
    image_list = get_object_or_404(ImageList, name=list_name)

    # Query all images in that list, ordered by position
    image_entries = ImageInList.objects.filter(image_list=image_list).select_related('image')

    # Return image URLs and positions
    data = [
        {
            'id': entry.image.id,
            'url': entry.image.image.url,
            'position': entry.position
        }
        for entry in image_entries
    ]

    return JsonResponse({'images': data})


@require_POST
def remove_image(request, list_name):
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
    try:
        image_id = int(request.POST['image_id'])
    except (KeyError, ValueError):
        return JsonResponse({'status': 'error', 'message': 'Invalid image_id'}, status=400)

    image_list = get_object_or_404(ImageList, name=list_name)
    try:
        entry = ImageInList.objects.get(image_id=image_id, image_list=image_list)
    except ImageInList.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Image not found in list'}, status=404)

    deleted_position = entry.position
    entry.delete()

    # Reorder remaining items
    ImageInList.objects.filter(
        image_list=image_list,
        position__gt=deleted_position
    ).update(position=F('position') - 1)

    return JsonResponse({'status': 'success'})
'''
