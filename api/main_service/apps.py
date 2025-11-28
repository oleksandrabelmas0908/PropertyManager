from django.apps import AppConfig

from broker import on_startup

class MainServiceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "main_service"

    def ready(self):
        on_startup()
