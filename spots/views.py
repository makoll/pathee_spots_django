from datetime import datetime, timedelta

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic

from .forms import SearchForm, SpotForm
from .models import Spot


class IndexView(generic.ListView):
    template_name = "spots/index.html"
    context_object_name = "spot_list"
    success_url = "/spots"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_form = SearchForm()
        context["search_form"] = search_form

        return context

    def get_queryset(self):

        default_display_count = 20

        spots = Spot.objects

        params = self.request.GET
        search_param_keys = (
            "id",
            "name",
            "branch",
            "business_status",
            "published_time_year",
            "published_time_month",
            "published_time_day",
        )
        search_params = {k: params[k] for k in search_param_keys if k in params}

        id = search_params.get("id")
        if id:
            spots = spots.filter(id=id)

        name = search_params.get("name")
        if name:
            spots = spots.filter(name__icontains=name)

        branch = search_params.get("branch")
        if branch:
            spots = spots.filter(branch__icontains=branch)

        business_status = search_params.get("business_status")
        if business_status:
            spots = spots.filter(business_status=business_status)

        published_time_year = search_params.get("published_time_year")
        published_time_month = search_params.get("published_time_month")
        published_time_day = search_params.get("published_time_day")

        if published_time_year and published_time_month and published_time_day:
            date = datetime(int(published_time_year), int(published_time_month), int(published_time_day))
            next_date = date + timedelta(days=1)
            spots = spots.filter(published_time__gte=date, published_time__lte=next_date)

        order = params.get("order")
        if not order:
            order = "id"

        order_direction = params.get("order_direction")
        if not order_direction:
            order_direction = ""

        display_count = default_display_count

        return spots.order_by(f"{order_direction}{order}")[:display_count]


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
