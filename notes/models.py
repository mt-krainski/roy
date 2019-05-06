import uuid as uuid
from django.conf import settings
from django.db import models
from django.utils.timezone import now
from markdownx.models import MarkdownxField


class Note(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)
    note = MarkdownxField()

    def save(self, *args, **kwargs):
        self.updated_at = now()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'
        permissions = (
            ('add', 'Add Notes'),
            ('modify', 'Modify Notes'),
            ('remove', 'Remove Notes'),
        )
