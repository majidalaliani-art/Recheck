from django.apps import AppConfig


class AdminConfig(AppConfig):
    name = 'Admin'
    def ready(self):
        import Admin.signals
