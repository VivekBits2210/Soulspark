from django.apps import AppConfig


class ChatModuleConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "chat_module"

    def ready(self):
        import soulspark_backend.celery_app
