# Generated by Django 5.0.3 on 2024-06-25 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vendor", "0010_alter_openinghour_from_hour_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vendor",
            name="vendor_slug",
            field=models.SlugField(max_length=255),
        ),
    ]