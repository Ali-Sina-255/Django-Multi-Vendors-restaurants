# Generated by Django 5.0.3 on 2024-07-19 18:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("marketplace", "0002_cart_delete_marketplace"),
        ("menu", "0002_alter_footitem_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="food_item",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="items",
                to="menu.footitem",
            ),
        ),
    ]
