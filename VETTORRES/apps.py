from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class VETTORRESConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'VETTORRES'
    verbose_name = _('VETTORRES')

    def ready(self):
        import VETTORRES.signals 
