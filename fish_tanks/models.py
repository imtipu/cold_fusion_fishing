from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from modules.model_mixins import TimeStampModel


class FishTank(TimeStampModel):
    title = models.CharField(_('Title'), max_length=255)
    tank_number = models.PositiveIntegerField(_('Tank Number'), unique=True)
    description = models.TextField(_('Description'), blank=True)
    volume = models.PositiveIntegerField()

    is_active = models.BooleanField(_('Active'), default=False)

    current_project = models.ForeignKey(
        'projects.Project',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Current Project'),
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Fish Tank')
        verbose_name_plural = _('Fish Tanks')
        ordering = ['title']

    def get_absolute_url(self):
        return reverse('dashboard:fish_tanks:fish_tank_detail', kwargs={'pk': self.pk})
