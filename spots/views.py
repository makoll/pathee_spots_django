from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic

from .forms import SpotForm
from .models import Spot


class IndexView(generic.ListView):
    template_name = "spots/index.html"
    context_object_name = "spot_list"

    def get_queryset(self):
        return Spot.objects.order_by("-id")[:5]


class DetailView(generic.DetailView):
    model = Spot
    template_name = "spots/detail.html"


def register(request, spot_id):
    spot = get_object_or_404(Spot, pk=spot_id)
    for key, value in request.POST.items():
        if hasattr(spot, key):
            if not value:
                value = None
            setattr(spot, key, value)
    spot.save()
    return HttpResponseRedirect(reverse("spots:detail", args=(spot.id,)))


class CreateView(generic.CreateView):
    model = Spot
    form_class = SpotForm
    template_name = "spots/create.html"
    success_url = "/spots"

    def form_valid(self, form):
        self.object = form.save(False)
        self.object.published_time = datetime.today()
        self.object.save()
        return super().form_valid(form)


class UpdateView(generic.UpdateView):
    model = Spot
    form_class = SpotForm
    template_name = "spots/update.html"
    success_url = "/spots"

    def form_valid(self, form):
        self.object = form.save(False)
        self.object.published_time = datetime.today()
        self.object.save()
        return super().form_valid(form)
