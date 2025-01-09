from django.apps import AppConfig


class RemitosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "remitos"

class RemitosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'remitos'

    def ready(self):
        import remitos.signals  # Asegúrate de conectar las señales aquí