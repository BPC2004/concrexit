# Generated by Django 4.1.7 on 2023-03-07 11:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("members", "0042_profile_is_minimized_alter_profile_address_city_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="shoesize",
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(39),
                    django.core.validators.MaxValueValidator(47),
                ],
                verbose_name="Shoe size",
            ),
        ),
    ]
