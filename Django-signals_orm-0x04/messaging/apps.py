from django.apps import AppConfig


class MessagingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "messaging"

    def ready(self):
        """
        This method is called when the app is ready.
        We can import signals here to ensure they are registered.
        """
        import messaging.signals
