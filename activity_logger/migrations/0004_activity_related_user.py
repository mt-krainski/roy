# Generated by Django 2.1.7 on 2019-03-24 11:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activity_logger', '0003_activity_activity_hash'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='related_user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
