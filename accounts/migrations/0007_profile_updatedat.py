# Generated by Django 4.2.4 on 2023-09-11 15:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0006_profile_first_name_profile_last_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="updatedAt",
            field=models.DateTimeField(auto_now=True),
        ),
    ]