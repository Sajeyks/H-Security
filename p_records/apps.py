from django.apps import AppConfig


class PRecordsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'p_records'

    def ready(self):
        import p_records.signals