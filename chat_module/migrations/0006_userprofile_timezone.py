# Generated by Django 4.1.7 on 2023-03-15 04:35

import chat_module.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat_module", "0005_remove_chathistory_progress_alter_chathistory_level"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="timezone",
            field=models.CharField(
                default="America/New_York",
                max_length=32,
                validators=[chat_module.models.timezone_validation],
            ),
        ),
    ]