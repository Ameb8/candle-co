from rest_framework import viewsets
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Max, F
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_POST
# from .permissions import IsAdminOrReadOnly
from .models import DesignImage, ImageList, ImageInList


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
        # Moving up → shift down others in between
        ImageInList.objects.filter(
            image_list=image_list,
            position__gte=new_position,
            position__lt=old_position
        ).update(position=F('position') + 1)
    else:
        # Moving down → shift up others in between
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

