# Generated by Django 5.1.4 on 2025-01-15 15:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clientes", "0004_cliente_created_at_cliente_created_by_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Departamento",
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
                ("descripcion", models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name="contacto",
            name="departamento",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="clientes.departamento",
            ),
        ),
    ]