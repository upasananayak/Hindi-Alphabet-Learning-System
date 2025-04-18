# Generated by Django 5.1 on 2025-03-12 10:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("alphabet", "0003_letterimage_audio_path"),
    ]

    operations = [
        migrations.CreateModel(
            name="TestLetters",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("order", models.IntegerField()),
                ("letter_path", models.CharField(max_length=255)),
                (
                    "object_path",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
            ],
        ),
    ]
