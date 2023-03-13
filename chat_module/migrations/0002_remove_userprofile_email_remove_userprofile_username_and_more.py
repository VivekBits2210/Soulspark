# Generated by Django 4.1.7 on 2023-03-13 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat_module", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="email",
        ),
        migrations.RemoveField(
            model_name="userprofile",
            name="username",
        ),
        migrations.AddField(
            model_name="userprofile",
            name="name",
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
    ]
