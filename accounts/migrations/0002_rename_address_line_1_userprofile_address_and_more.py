# Generated by Django 4.2 on 2024-05-13 07:55

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="userprofile",
            old_name="address_line_1",
            new_name="address",
        ),
        migrations.RemoveField(
            model_name="userprofile",
            name="address_line_2",
        ),
    ]
