# Generated by Django 5.0.3 on 2024-05-28 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vendor", "0005_alter_openinghour_day"),
    ]

    operations = [
        migrations.AlterField(
            model_name="openinghour",
            name="day",
            field=models.IntegerField(
                choices=[
                    (1, "Saturday"),
                    (2, "Sunday"),
                    (3, "Monday"),
                    (4, "Tuesday"),
                    (5, "Wednesday"),
                    (6, "Thursday"),
                    (7, "Friday"),
                ]
            ),
        ),
    ]
