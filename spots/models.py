from enum import Enum

from django.db import models


class BusinessStatus(Enum):
    closed = 'Closed'


class Spot(models.Model):
    name = models.CharField(max_length=255, default=None, blank=True)
    name_sub = models.CharField(max_length=255, default=None, blank=True)
    branch = models.CharField(max_length=255, default=None, blank=True)
    # center = Column(Point, nullable=False, blank=True)
    address = models.CharField(max_length=255, default=None, blank=True)
    building = models.CharField(max_length=255, default=None, blank=True)
    phone = models.CharField(max_length=255, default=None, blank=True)
    description = models.TextField(default=None, blank=True)
    business_status = models.CharField(
        max_length=255, choices=[(tag, tag.value) for tag in BusinessStatus], blank=True, null=True)
    business_status_confirm_time = models.DateTimeField(blank=True, null=True)
    business_hour = models.TextField(default=None, blank=True)
    published_time = models.DateTimeField(blank=True, null=True)

    def __str__(self, blank=True):
        return f'{self.name} : {self.branch}'
