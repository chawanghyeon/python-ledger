# Generated by Django 3.2.14 on 2023-04-05 20:34

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("ledgers", "0002_ledger_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="sharedledger",
            name="created_at",
        ),
    ]