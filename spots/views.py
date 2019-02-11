from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Spot


def index(request):
    spot_list = Spot.objects.order_by('-id')[:5]
    context = {'spot_list': spot_list}
    return render(request, 'spots/index.html', context)


def detail(request, spot_id):
    spot = get_object_or_404(Spot, pk=spot_id)
    return render(request, 'spots/detail.html', {'spot': spot})


def register(request, spot_id):
    spot = get_object_or_404(Spot, pk=spot_id)
    for key, value in request.POST.items():
        if hasattr(spot, key):
            if not value:
                value = None
            setattr(spot, key, value)
    spot.save()
    return HttpResponseRedirect(reverse('spots:detail', args=(spot.id, )))
