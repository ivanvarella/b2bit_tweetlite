from django.apps import AppConfig


class TweetsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tweets"

    def ready(self):
        """Import signals when Django starts."""
        import tweets.signals
