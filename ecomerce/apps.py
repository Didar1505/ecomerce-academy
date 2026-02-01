from django.apps import AppConfig


class EcomerceConfig(AppConfig):
    name = 'ecomerce'

    def ready(self):
        from . import signals