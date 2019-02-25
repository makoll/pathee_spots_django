from django import forms

from .models import Spot


class SpotForm(forms.ModelForm):

    class Meta:
        model = Spot
        fields = (
            'name',
            'name_sub',
            'branch',
            'lat',
            'lng',
            'address',
            'building',
            'phone',
            'description',
            'business_status',
            'business_status_confirm_time',
            'business_hour',
        )
