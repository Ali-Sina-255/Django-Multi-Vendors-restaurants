# Generated by Django 5.0.3 on 2024-05-28 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vendor", "0006_alter_openinghour_day"),
    ]

    operations = [
        migrations.AlterField(
            model_name="openinghour",
            name="day",
            field=models.IntegerField(
                choices=[
                    (1, "Monday"),
                    (2, "Tuesday"),
                    (3, "Wednesday"),
                    (4, "Thursday"),
                    (5, "Friday"),
                    (6, "Saturday"),
                    (7, "Sunday"),
                ]
            ),
        ),
    ]
