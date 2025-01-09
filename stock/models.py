from django.db import models

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


# Modelo para Stock
class Stock(models.Model):
    producto = models.ForeignKey('productos.Producto', on_delete=models.CASCADE)  # Producto relacionado
    deposito = models.ForeignKey(Deposito, on_delete=models.CASCADE)  # Depósito relacionado
    cantidad = models.PositiveIntegerField()  # Cantidad disponible

    def __str__(self):
        return f"{self.producto} - {self.deposito} - {self.cantidad}"
