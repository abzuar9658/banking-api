# Generated by Django 4.2.15 on 2025-05-12 17:45

import core_apps.user_auth.managers
from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        max_length=50, unique=True, verbose_name="Username"
                    ),
                ),
                (
                    "security_question",
                    models.CharField(
                        choices=[
                            ("favorite_color", "Favorite Color"),
                            ("first_pet", "First Pet"),
                            ("mother_maiden_name", "Mother's Maiden Name"),
                            ("birth_city", "Birth City"),
                            ("childhood_friend", "Childhood Friend"),
                        ],
                        max_length=50,
                        verbose_name="Security Question",
                    ),
                ),
                (
                    "security_answer",
                    models.CharField(max_length=100, verbose_name="Security Answer"),
                ),
                (
                    "email",
                    models.EmailField(db_index=True, max_length=254, unique=True),
                ),
                (
                    "first_name",
                    models.CharField(max_length=30, verbose_name="First Name"),
                ),
                (
                    "middle_name",
                    models.CharField(
                        blank=True, max_length=30, verbose_name="Middle Name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(max_length=30, verbose_name="Last Name"),
                ),
                (
                    "id_no",
                    models.PositiveBigIntegerField(
                        unique=True, verbose_name="ID Number"
                    ),
                ),
                (
                    "account_status",
                    models.CharField(
                        choices=[
                            ("active", "Active"),
                            ("locked", "Locked"),
                            ("inactive", "Inactive"),
                        ],
                        default="active",
                        max_length=50,
                        verbose_name="Account Status",
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("customer", "Customer"),
                            ("account_executive", "Account Executive"),
                            (
                                "customer_service_representative",
                                "Customer Service Representative",
                            ),
                            ("bank_teller", "Bank Teller"),
                            ("bank_manager", "Bank Manager"),
                            ("bank_administrator", "Bank Administrator"),
                            ("bank_auditor", "Bank Auditor"),
                            ("bank_technician", "Bank Technician"),
                            ("bank_security_guard", "Bank Security Guard"),
                        ],
                        default="customer",
                        max_length=50,
                        verbose_name="Role",
                    ),
                ),
                (
                    "failed_login_attempts",
                    models.PositiveSmallIntegerField(
                        default=0, verbose_name="Failed Login Attempts"
                    ),
                ),
                (
                    "last_failed_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Last Failed Login"
                    ),
                ),
                (
                    "otp",
                    models.CharField(
                        blank=True, max_length=6, null=True, verbose_name="OTP"
                    ),
                ),
                (
                    "otp_expiry",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="OTP Expiry"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(default=False, verbose_name="Is Superuser"),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="Date Joined"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="Created At"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated At"),
                ),
            ],
            options={
                "verbose_name": "User",
                "verbose_name_plural": "Users",
                "ordering": ["-date_joined", "-created_at"],
            },
            managers=[
                ("objects", core_apps.user_auth.managers.UserManager()),
            ],
        ),
    ]
