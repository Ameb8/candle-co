from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.db.models.functions import TruncDate
from django.db.models import Count, Sum
from orders.models import Order, OrderItem

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def orders_over_time(request):
    orders_by_date = (
        Order.objects
        .annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )

    # Prepare data as lists
    dates = [entry['date'] for entry in orders_by_date]
    counts = [entry['count'] for entry in orders_by_date]

    # Serialize dates as ISO strings
    dates = [d.isoformat() if d else None for d in dates]

    return Response({
        'dates': dates,
        'counts': counts,
    })

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def orders_by_category(request):
    data = (
        OrderItem.objects
        .values('product__category')
        .annotate(total_quantity=Sum('quantity'))
        .order_by('product__category')
    )

    # Data to track
    categories = [entry['product__category'] or 'Uncategorized' for entry in data]
    quantities = [entry['total_quantity'] for entry in data]

    return Response({
        'categories': categories,
        'quantities': quantities,
    })
