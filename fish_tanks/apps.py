from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FishTanksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fish_tanks'
    verbose_name = _('Fish Tanks')

    def ready(self):
        try:
            import fish_tanks.signals  # noqa F401
        except ImportError:
            pass
