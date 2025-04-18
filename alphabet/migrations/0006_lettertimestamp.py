# Generated by Django 5.1 on 2025-03-18 22:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("alphabet", "0005_remove_letterimage_audio_path"),
    ]

    operations = [
        migrations.CreateModel(
            name="LetterTimestamp",
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
                ("letter", models.CharField(max_length=10)),
                (
                    "letter_type",
                    models.CharField(
                        choices=[("vowel", "Vowel"), ("consonant", "Consonant")],
                        max_length=10,
                    ),
                ),
                ("start_time", models.IntegerField()),
                ("end_time", models.IntegerField()),
                ("order", models.IntegerField()),
            ],
        ),
    ]
