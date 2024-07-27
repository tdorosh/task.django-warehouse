from django.core.exceptions import ValidationError
from django.db import models

from tasks.models import Task


class Sparepart(models.Model):

    name = models.CharField(max_length=256, unique=True)
    units = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    replaceable_with = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
    )

    def __str__(self):
        return f'{self.name}'


class PlannedSparepart(models.Model):

    task = models.ForeignKey(Task, on_delete=models.PROTECT)
    sparepart = models.OneToOneField(Sparepart, on_delete=models.PROTECT)
    planned_amount = models.PositiveIntegerField()
    current_amount = models.PositiveIntegerField(blank=True, default=0)

    def clean(self):
        if self.current_amount > self.planned_amount:
            raise ValidationError('Current amount can not be greater that planned.')

    def __str__(self):
        return f'{self.task}, {self.sparepart}'


class SparepartBalance(models.Model):

    sparepart = models.OneToOneField(Sparepart, on_delete=models.PROTECT)
    amount = models.PositiveIntegerField()
    warehouse = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.sparepart}: {self.amount}, {self.warehouse}'
