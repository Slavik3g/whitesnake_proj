# Generated by Django 4.2.3 on 2023-07-14 08:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("carshowroom", "0001_initial"),
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CustomerModel",
            fields=[
                ("is_active", models.BooleanField(default=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "balance",
                    models.DecimalField(decimal_places=2, default=0, max_digits=19),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Customer",
                "verbose_name_plural": "Customers",
                "db_table": "customer",
            },
        ),
        migrations.CreateModel(
            name="CustomerPurchaseHistoryModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "price",
                    models.DecimalField(decimal_places=3, default=0, max_digits=10),
                ),
                (
                    "car",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT, to="core.carmodel"
                    ),
                ),
                (
                    "car_showroom",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="carshowroom.carshowroommodel",
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="customers.customermodel",
                    ),
                ),
            ],
            options={
                "verbose_name": "CustomerPurchaseHistory",
                "verbose_name_plural": "CustomerPurchaseHistories",
                "db_table": "customer_purchase_history",
            },
        ),
        migrations.AddField(
            model_name="customermodel",
            name="purchase_history",
            field=models.ManyToManyField(
                through="customers.CustomerPurchaseHistoryModel",
                to="carshowroom.carshowroommodel",
            ),
        ),
    ]
