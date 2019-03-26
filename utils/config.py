from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_save


class RoyConfig(AppConfig):
    """Configuration class.

    The ready method is executed during django startup.
    """
    name = 'roy'
    verbose_name = "Roy"

    @staticmethod
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        """Creat an auth token for a newly created user instance."""
        from rest_framework.authtoken.models import Token
        if created:
            Token.objects.create(user=instance)

    def ready(self):
        """Connect the post-save action to the user model."""
        post_save.connect(
            self.create_auth_token, sender=settings.AUTH_USER_MODEL)
