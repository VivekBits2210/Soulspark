# Generated by Django 4.1.7 on 2023-03-13 00:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ai_profiles", "0004_alter_botprofile_profession"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="botprofile",
            name="profession",
        ),
    ]
