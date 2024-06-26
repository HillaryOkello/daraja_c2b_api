# Generated by Django 5.0.4 on 2024-05-07 12:43

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="C2BTransaction",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("short_code", models.CharField(max_length=10)),
                (
                    "response_type",
                    models.CharField(blank=True, max_length=10, null=True),
                ),
                ("confirmation_url", models.URLField(blank=True, null=True)),
                ("validation_url", models.URLField(blank=True, null=True)),
                ("command_id", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "amount",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("msisdn", models.CharField(blank=True, max_length=15, null=True)),
                (
                    "bill_ref_number",
                    models.CharField(blank=True, max_length=50, null=True, unique=True),
                ),
                (
                    "originator_conversation_id",
                    models.CharField(blank=True, max_length=36, null=True),
                ),
                (
                    "transaction_id",
                    models.CharField(blank=True, max_length=36, null=True),
                ),
                ("transaction_time", models.DateTimeField(blank=True, null=True)),
                (
                    "invoice_number",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "validation_response_sent",
                    models.BooleanField(blank=True, default=False, null=True),
                ),
                (
                    "default_action",
                    models.CharField(
                        choices=[
                            ("Completed", "Completed"),
                            ("Cancelled", "Cancelled"),
                        ],
                        default="Completed",
                        max_length=10,
                    ),
                ),
                (
                    "response_code",
                    models.CharField(blank=True, max_length=3, null=True),
                ),
                ("response_description", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
