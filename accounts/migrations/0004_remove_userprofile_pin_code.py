# Generated by Django 5.0.3 on 2024-07-25 12:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_remove_userprofile_country"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="pin_code",
        ),
    ]
