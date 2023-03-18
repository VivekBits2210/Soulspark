# Generated by Django 4.1.7 on 2023-03-17 12:29

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("ai_profiles", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("dialog_engine", "0002_rename_promptrecord_gptusagerecord"),
    ]

    operations = [
        migrations.RenameField(
            model_name="gptusagerecord",
            old_name="indicator_cost",
            new_name="indicator_tokens",
        ),
        migrations.RenameField(
            model_name="gptusagerecord",
            old_name="indicator_tuple",
            new_name="indicator_vector",
        ),
        migrations.RenameField(
            model_name="gptusagerecord",
            old_name="story_cost",
            new_name="story_tokens",
        ),
        migrations.RenameField(
            model_name="gptusagerecord",
            old_name="total_cost",
            new_name="total_tokens",
        ),
        migrations.AlterUniqueTogether(
            name="gptusagerecord",
            unique_together={("user", "bot", "chat_history_length")},
        ),
    ]