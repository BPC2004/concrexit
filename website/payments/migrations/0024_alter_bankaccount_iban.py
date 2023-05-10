# Generated by Django 4.2.1 on 2023-05-10 18:29

from django.db import migrations
import localflavor.generic.models


class Migration(migrations.Migration):
    dependencies = [
        ("payments", "0023_payment_payable_model_payment_payable_object_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bankaccount",
            name="iban",
            field=localflavor.generic.models.IBANField(
                include_countries=(
                    "AD",
                    "AT",
                    "BE",
                    "BG",
                    "CH",
                    "CY",
                    "CZ",
                    "DE",
                    "DK",
                    "EE",
                    "ES",
                    "FI",
                    "FR",
                    "GB",
                    "GI",
                    "GR",
                    "HR",
                    "HU",
                    "IE",
                    "IS",
                    "IT",
                    "LI",
                    "LT",
                    "LU",
                    "LV",
                    "MC",
                    "MT",
                    "NL",
                    "NO",
                    "PL",
                    "PT",
                    "RO",
                    "SE",
                    "SI",
                    "SK",
                    "SM",
                    "VA",
                ),
                max_length=34,
                use_nordea_extensions=False,
                verbose_name="IBAN",
            ),
        ),
    ]
