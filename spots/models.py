from enum import Enum
import re

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy


def validate_lat(value):
    if value < -90 or 90 < value:
        raise ValidationError(gettext_lazy(f"{value}は緯度として不適切です"))


def validate_lng(value):
    if value < -180 or 180 < value:
        raise ValidationError(gettext_lazy(f"{value}は経度として不適切です"))


def validate_phone(value):
    rep = r"^0\d{1,2}-\d{4}-\d{4}$"
    if re.match(rep, value) is None:
        raise ValidationError(gettext_lazy(f"{value}は電話番号として不適切です"))


def validate_url(value):
    rep = r"^https?(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+\$,%#]+)$"
    if re.match(rep, value) is None:
        raise ValidationError(gettext_lazy(f"{value}はURLとして不適切です"))


class BusinessStatus(Enum):
    closed = "Closed"


class Spot(models.Model):
    name = models.CharField(max_length=255, default=None, blank=True)
    name_sub = models.CharField(max_length=255, default=None, blank=True)
    branch = models.CharField(max_length=255, default=None, blank=True)
    lat = models.DecimalField(
        "緯度",
        max_digits=8,
        decimal_places=6,
        default=None,
        blank=True,
        validators=[validate_lat],
    )
    lng = models.DecimalField(
        "経度",
        max_digits=9,
        decimal_places=6,
        default=None,
        blank=True,
        validators=[validate_lng],
    )
    address = models.CharField(max_length=255, default=None, blank=True)
    building = models.CharField(max_length=255, default=None, blank=True)
    phone = models.CharField(
        max_length=255, default=None, blank=True, validators=[validate_phone]
    )
    description = models.TextField(default=None, blank=True)
    business_status = models.CharField(
        max_length=255,
        choices=[(tag, tag.value) for tag in BusinessStatus],
        blank=True,
        null=True,
    )
    business_status_confirm_time = models.DateTimeField(blank=True, null=True)
    business_hour = models.TextField(default=None, blank=True)
    published_time = models.DateTimeField(blank=True, null=True)

    def __str__(self, blank=True):
        return f"{self.name} : {self.branch}"


class Url(models.Model):
    order = models.IntegerField("順番")
    url = models.TextField("URL", validators=[validate_url])
    spot = models.ForeignKey(Spot, verbose_name="紐づくスポット", on_delete=models.CASCADE)
