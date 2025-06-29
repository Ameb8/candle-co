import plotly.graph_objs as go
import plotly.offline as opy
from django.http import HttpResponse
from django.db.models.functions import TruncDate
from django.db.models import Count
from orders.models import Order


def orders_over_time(request):
    orders_by_date = (
        Order.objects
        .annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )

    dates = [entry['date'] for entry in orders_by_date]
    counts = [entry['count'] for entry in orders_by_date]

    trace = go.Scatter(x=dates, y=counts, mode='lines+markers', name='Orders')
    layout = go.Layout(title='Orders Over Time', xaxis=dict(title='Date'), yaxis=dict(title='Number of Orders'))
    fig = go.Figure(data=[trace], layout=layout)


    plot_div = opy.plot(fig, auto_open=False, output_type='div', include_plotlyjs=False)

    return HttpResponse(plot_div)

