from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from modules.model_mixins import TimeStampModel


class FishTank(TimeStampModel):
    title = models.CharField(_('Title'), max_length=255)
    tank_number = models.PositiveIntegerField(_('Tank Number'), unique=True)
    description = models.TextField(_('Description'), blank=True)
    volume = models.PositiveIntegerField()
    length = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    width = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    height = models.DecimalField(default=0, decimal_places=2, max_digits=10)

    capacity = models.DecimalField(default=0, decimal_places=2, max_digits=10)

    is_active = models.BooleanField(_('Active'), default=False)

    current_project = models.ForeignKey(
        'projects.Project',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Fish Tank'
        verbose_name_plural = 'Fish Tanks'
        ordering = ['title']

    def get_absolute_url(self):
        return reverse('dashboard:fish_tanks:fish_tank_detail', kwargs={'pk': self.pk})
