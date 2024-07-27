from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class TaskStatuses(models.TextChoices):

    PLANNED = "PL", "PLANNED"
    REVIEW = "RE", "REVIEW"
    IN_PROGRESS = "IP", "IN_PROGRESS"
    DONE = "DN", "DONE"


class Task(models.Model):

    status = models.CharField(
        max_length=10,
        choices=TaskStatuses,
        default=TaskStatuses.PLANNED,
    )
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    done = models.DateTimeField(null=True, blank=True)
    scheduled = models.DateTimeField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='created_tasks',
    )
    assigned = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='assigned_tasks',
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.author}: {self.scheduled} -> {self.assigned}: {self.status}'
