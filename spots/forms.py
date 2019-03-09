from django.forms import ModelForm, inlineformset_factory
from django.forms.widgets import TextInput

from .models import Spot, Url


class ModelFormWithFormSetMixin:
    def __init__(self, *args, **kwargs):
        super(ModelFormWithFormSetMixin, self).__init__(*args, **kwargs)
        self.formset = self.formset_class(instance=self.instance, data=self.data if self.is_bound else None)

    def is_valid(self):
        return super(ModelFormWithFormSetMixin, self).is_valid() and self.formset.is_valid()

    def save(self, commit=True):
        saved_instance = super(ModelFormWithFormSetMixin, self).save(commit)
        self.formset.save(commit)
        return saved_instance


class UrlForm(ModelForm):
    class Meta:
        model = Url
        fields = ("url",)
        widgets = {"url": TextInput}

    def save(self, commit=True):
        instance = super(UrlForm, self).save(commit=False)
        instance.order = self.cleaned_data.get("ORDER")
        if commit:
            instance.save()
        return instance


UrlFormSet = inlineformset_factory(
    parent_model=Spot, model=Url, form=UrlForm, fields=("url",), max_num=1, can_order=True, can_delete=False
)


class SpotForm(ModelFormWithFormSetMixin, ModelForm):

    formset_class = UrlFormSet

    class Meta:
        model = Spot
        fields = (
            "name",
            "name_sub",
            "branch",
            "lat",
            "lng",
            "address",
            "building",
            "phone",
            "description",
            "business_status",
            "business_status_confirm_time",
            "business_hour",
        )
