
from django.apps import AppConfig
from django.core.signals import request_finished


class XauthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "xauth"
    verbose_name = "Gestion des utilisateurs"

    def ready(self):
        from xauth import signals
        from xauth.models import User