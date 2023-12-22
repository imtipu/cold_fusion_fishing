from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from modules.model_mixins import TimeStampModel


class ProjectStatusTypes(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'
    COMPLETED = 'completed', 'Completed'
    closed = 'closed', 'Closed'


class Project(TimeStampModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    tank = models.ForeignKey(
        'fish_tanks.FishTank',
        on_delete=models.CASCADE,
        related_name='projects',
    )

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    initial_quantity = models.PositiveIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
        ]
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'


class DailyActivity(TimeStampModel):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='daily_activities',
    )

    activity_date = models.DateField()
    dead_fish = models.PositiveIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
        ]
    )

    single_fish_weight = models.DecimalField(
        _('Single Fish Weight (gm)'),
        max_digits=10,
        decimal_places=6,
        default=0,
        validators=[
            MinValueValidator(0),
        ]
    )

    feed_percentage = models.DecimalField(
        _('Feed Percentage (%)'),
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[
            MinValueValidator(0),
        ]
    )

    undigested_percentage = models.DecimalField(
        _('Undigested Percentage (%)'),
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[
            MinValueValidator(0),
        ]
    )

    feed_protein_percentage = models.DecimalField(
        _('Feed Protein Percentage (%)'),
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[
            MinValueValidator(0),
        ]
    )

    expected_cn = models.DecimalField(
        _('Expected C.N.'),
        max_digits=10,
        decimal_places=6,
        default=0,
        validators=[
            MinValueValidator(0),
        ]
    )

    live_fish = models.PositiveIntegerField(_('Live Fish'), default=0)

    def __str__(self):
        return f'{self.project.title} - {self.activity_date}'

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Daily Activity'
        verbose_name_plural = 'Daily Activities'

        constraints = [
            models.UniqueConstraint(
                fields=['project', 'activity_date'],
                name='unique_daily_activity'
            )
        ]

    @property
    def total_live_fish(self):
        return self.project.initial_quantity - self.dead_fish

    @property
    def total_weight(self):
        return round(self.live_fish * self.single_fish_weight, 2)

    @property
    def total_weight_kg(self):
        return round(self.total_weight / 1000, 2)

    @property
    def todays_feed(self):
        return round(self.total_weight * self.feed_percentage / 100, 4)

    @property
    def molas_to_add(self):
        value = (float(self.feed_n * float(self.expected_cn)) - float(self.feed_c)) / 0.28
        return round(value, 2)

    @property
    def feed_n(self):
        value = float(self.todays_feed) * 0.90 * float(self.undigested_percentage / 100) * float(
            self.feed_protein_percentage / 100) * 0.16
        return round(value, 10)

    @property
    def feed_c(self):
        value = float(self.todays_feed) * 0.90 * float(self.undigested_percentage / 100) * 0.5
        return round(value, 10)

    # def clean(self):
    #     data = super().clean()
    #     print(data)

    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         activity_date = self.activity_date
    #         project = self.project
    #         if DailyActivity.objects.filter(activity_date=activity_date, project=project).exists():
    #             raise ValueError(_('Daily activity for this date already exists.'))
    #     super().save(*args, **kwargs)
