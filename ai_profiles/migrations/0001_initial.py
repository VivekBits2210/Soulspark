# Generated by Django 4.1.7 on 2023-03-24 00:29

import ai_profiles.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BotProfile",
            fields=[
                ("bot_id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "name",
                    models.CharField(
                        max_length=50, validators=[ai_profiles.models.validate_name]
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        max_length=1,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Gender must be either M or F", regex="^[MF]$"
                            )
                        ],
                    ),
                ),
                (
                    "age",
                    models.IntegerField(validators=[ai_profiles.models.validate_age]),
                ),
                ("bio", models.CharField(max_length=300)),
                ("profession", models.CharField(max_length=100)),
                (
                    "interests",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=250,
                        validators=[ai_profiles.models.interests_validation],
                    ),
                ),
                (
                    "favorites",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        validators=[ai_profiles.models.validate_dict],
                    ),
                ),
                (
                    "physical_attributes",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        validators=[ai_profiles.models.validate_dict],
                    ),
                ),
                (
                    "profile_image",
                    models.ImageField(
                        upload_to="images/",
                        validators=[ai_profiles.models.validate_image_extension],
                    ),
                ),
                ("searchable", models.BooleanField(default=True)),
                ("summary", models.TextField(blank=True, default="")),
            ],
        ),
    ]
