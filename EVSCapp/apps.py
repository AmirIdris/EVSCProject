from django.apps import AppConfig


class EvscappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'EVSCapp'

    def ready(self):
        import EVSCapp.signals
