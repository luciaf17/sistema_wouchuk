from django.db import models
from utils.audit import AuditModel  # Importa el modelo base desde utils

# Modelo para Depósitos
class Deposito(models.Model):
    descripcion = models.TextField()  # Nombre del depósito
    ubicacion = models.TextField(null=True, blank=True)  # Ubicación física

    def __str__(self):
        return self.descripcion


# Modelo para Pasillos
class Pasillo(models.Model):
    descripcion = models.TextField()  # Identificación del pasillo

    def __str__(self):
        return self.descripcion


# Modelo para Columnas
class Columna(models.Model):
    descripcion = models.TextField()  # Identificación de la columna

    def __str__(self):
        return self.descripcion


# Modelo para Estantes
class Estante(models.Model):
    descripcion = models.TextField()  # Identificación del estante

    def __str__(self):
        return self.descripcion


class Stock(models.Model):
    producto = models.ForeignKey('productos.Producto', on_delete=models.CASCADE, verbose_name="Producto")
    deposito = models.ForeignKey(Deposito, on_delete=models.CASCADE, verbose_name="Depósito")
    cantidad = models.PositiveIntegerField(default=0, verbose_name="Cantidad")

    class Meta:
        indexes = [
            models.Index(fields=['producto', 'deposito'], name='idx_producto_deposito'),
        ]

    def __str__(self):
        return f"{self.producto.descripcion} - {self.deposito.descripcion} - {self.cantidad}"
