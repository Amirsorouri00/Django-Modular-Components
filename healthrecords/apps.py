from django.apps import AppConfig


class HealthrecordsConfig(AppConfig):
    name = 'healthrecords'

    def ready(self):
        import healthrecords.signals