# Generated by Django 4.1.7 on 2023-03-29 07:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("user_profiles", "0003_alter_userprofile_user"),
        ("chat_module", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chathistory",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="user_profiles.user"
            ),
        ),
        migrations.AlterField(
            model_name="deletedchathistory",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="user_profiles.user"
            ),
        ),
    ]
