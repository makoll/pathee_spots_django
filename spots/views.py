from django.shortcuts import get_object_or_404, render

from .models import Spot


def index(request):
    spot_list = Spot.objects.order_by('-id')[:5]
    context = {'spot_list': spot_list}
    return render(request, 'spots/index.html', context)


def detail(request, spot_id):
    spot = get_object_or_404(Spot, pk=spot_id)
    return render(request, 'spots/detail.html', {'spot': spot})
