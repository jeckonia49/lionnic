# Generated by Django 4.2.4 on 2023-08-08 09:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0002_alter_postcomment_post"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="bg_image",
            field=models.ImageField(blank=True, null=True, upload_to="bg_posts/"),
        ),
    ]
