from django.apps import AppConfig


class EngineerConfig(AppConfig):
    name = 'Engineer'
    def ready(self):
        import Engineer.signals
