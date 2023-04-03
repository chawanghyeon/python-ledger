# Generated by Django 4.2 on 2023-04-04 02:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("custom_types", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Ledger",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=50)),
                ("memo", models.CharField(blank=True, max_length=100)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("date", models.DateField()),
                (
                    "type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="custom_types.customtype",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Ledgers",
                "ordering": ["-date", "-id"],
            },
        ),
    ]
