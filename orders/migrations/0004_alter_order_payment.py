# Generated by Django 5.0.3 on 2024-06-06 05:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0003_remove_order_tax_data"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="payment",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="orders.payment",
            ),
        ),
    ]
