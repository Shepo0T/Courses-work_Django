# Generated by Django 5.1.2 on 2024-10-24 14:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Client",
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
                ("FIO", models.CharField(max_length=150, verbose_name="ФИО")),
                (
                    "email",
                    models.EmailField(
                        max_length=150, unique=True, verbose_name="почта"
                    ),
                ),
                (
                    "comment",
                    models.TextField(blank=True, null=True, verbose_name="комментарий"),
                ),
            ],
            options={
                "verbose_name": "клиент",
                "verbose_name_plural": "клиенты",
                "ordering": ("FIO",),
            },
        ),
        migrations.CreateModel(
            name="MailingSettings",
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
                (
                    "start_time",
                    models.DateTimeField(verbose_name="время начала рассылки"),
                ),
                (
                    "end_time",
                    models.DateTimeField(verbose_name="время окончания рассылки"),
                ),
                (
                    "periodicity",
                    models.CharField(
                        choices=[
                            ("Раз в день", "Раз в день"),
                            ("Раз в неделю", "Раз в неделю"),
                            ("Раз в месяц", "Раз в месяц"),
                        ],
                        max_length=50,
                        verbose_name="периодичность",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Завершена", "Завершена"),
                            ("Создана", "Создана"),
                            ("Запущена", "Запущена"),
                        ],
                        default="Создана",
                        max_length=50,
                        verbose_name="статус рассылки",
                    ),
                ),
                (
                    "clients",
                    models.ManyToManyField(
                        to="mailings.client", verbose_name="клиенты рассылки"
                    ),
                ),
            ],
            options={
                "verbose_name": "настройки рассылки",
                "verbose_name_plural": "настройки рассылки",
                "permissions": [("change_status", "Can change status")],
            },
        ),
        migrations.CreateModel(
            name="Log",
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
                (
                    "time",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="дата и время последней попытки"
                    ),
                ),
                ("status", models.BooleanField(verbose_name="статус попытки")),
                (
                    "server_response",
                    models.CharField(
                        blank=True, null=True, verbose_name="ответ почтового сервера"
                    ),
                ),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mailings.client",
                        verbose_name="клиент рассылки",
                    ),
                ),
                (
                    "mailing_list",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mailings.mailingsettings",
                        verbose_name="рассылка",
                    ),
                ),
            ],
            options={
                "verbose_name": "лог",
                "verbose_name_plural": "логи",
            },
        ),
        migrations.CreateModel(
            name="Message",
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
                ("title", models.CharField(max_length=100, verbose_name="тема письма")),
                ("text", models.TextField(verbose_name="тело письма")),
                (
                    "mailing_list",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="messages",
                        to="mailings.mailingsettings",
                        verbose_name="рассылка",
                    ),
                ),
            ],
            options={
                "verbose_name": "сообщение",
                "verbose_name_plural": "сообщения",
            },
        ),
    ]