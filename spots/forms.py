from django import forms
from django.forms import ModelForm, inlineformset_factory
from django.forms.widgets import TextInput

from .models import BusinessStatus, Spot, Url


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


business_status_choices = [(tag.name, tag.value) for tag in BusinessStatus]
business_status_choices.insert(0, (None, "-" * 10))
order_choices = (("id", "id"), ("published_time", "published_time"))
order_direction_choices = (("", "昇順"), ("-", "降順"))


class SearchForm(forms.Form):

    id = forms.DecimalField(initial="", label="スポットID", required=False)
    name = forms.CharField(initial="", label="名前", required=False)
    branch = forms.CharField(initial="", label="支店名", required=False)
    business_status = forms.ChoiceField(initial="", label="ステータス", required=False, choices=business_status_choices)
    published_time = forms.DateField(
        initial="",
        label="公開時間",
        required=False,
        widget=forms.SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")),
    )
    order = forms.ChoiceField(initial="id", label="ソート項目", widget=forms.RadioSelect, choices=order_choices)
    order_direction = forms.ChoiceField(initial="-", label="ソート方向", widget=forms.RadioSelect, choices=order_direction_choices)
