# Generated by Django 4.1.7 on 2023-03-14 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat_module", "0002_deletedchathistory"),
    ]

    operations = [
        migrations.AddField(
            model_name="chathistory",
            name="input_chars",
            field=models.IntegerField(default=0),
        ),
    ]