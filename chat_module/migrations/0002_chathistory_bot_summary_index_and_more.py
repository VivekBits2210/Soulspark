# Generated by Django 4.1.7 on 2023-03-17 06:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat_module", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="chathistory",
            name="bot_summary_index",
            field=models.IntegerField(default=1, null=True),
        ),
        migrations.AddField(
            model_name="chathistory",
            name="user_summary_index",
            field=models.IntegerField(default=-1, null=True),
        ),
    ]