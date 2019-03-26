from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_save



class RoyConfig(AppConfig):
    name = 'roy'
    verbose_name = "Roy"

    @staticmethod
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        from rest_framework.authtoken.models import Token
        if created:
            Token.objects.create(user=instance)

    def ready(self):
        """Initialized when application has started"""
        post_save.connect(self.create_auth_token, sender=settings.AUTH_USER_MODEL)
