# Generated by Django 2.1.7 on 2019-03-26 23:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity_logger', '0006_auto_20190324_1129'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activity',
            options={'permissions': (('add', 'Add activities via API'), ('remove', 'Remove activities via API')), 'verbose_name': 'Activity', 'verbose_name_plural': 'Activities'},
        ),
    ]