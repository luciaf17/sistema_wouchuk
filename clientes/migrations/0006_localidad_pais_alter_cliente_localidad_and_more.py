# Generated by Django 5.1.4 on 2025-01-15 15:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clientes", "0005_departamento_alter_contacto_departamento"),
    ]

    operations = [
        migrations.CreateModel(
            name="Localidad",
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
                ("cp", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Pais",
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
                ("cod_tel", models.TextField(blank=True, null=True)),
                ("gtm", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name="cliente",
            name="localidad",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="clientes.localidad",
            ),
        ),
        migrations.AddField(
            model_name="localidad",
            name="pais",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="clientes.pais"
            ),
        ),
        migrations.CreateModel(
            name="Provincia",
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
                (
                    "pais",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="clientes.pais"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="localidad",
            name="provincia",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="clientes.provincia"
            ),
        ),
    ]