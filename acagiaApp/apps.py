from django.apps import AppConfig


class AcagiaappConfig(AppConfig):
    name = 'acagiaApp'
    def ready(self):
        import acagiaApp.signals