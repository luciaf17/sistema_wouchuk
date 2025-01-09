from django.db import models
from utils.audit import AuditModel  # Importa el modelo base desde utils

# Modelo para Productos
class Producto(AuditModel):
    barcode = models.TextField(null=True, blank=True)  # Código de barras (puede repetirse)
    descripcion = models.TextField()  # Descripción del producto
    loc_dep = models.ForeignKey('stock.Deposito', on_delete=models.SET_NULL, null=True, blank=True)  # Depósito
    loc_pas = models.ForeignKey('stock.Pasillo', on_delete=models.SET_NULL, null=True, blank=True)  # Pasillo
    loc_col = models.ForeignKey('stock.Columna', on_delete=models.SET_NULL, null=True, blank=True)  # Columna
    loc_est = models.ForeignKey('stock.Estante', on_delete=models.SET_NULL, null=True, blank=True)  # Estante

    def __str__(self):
        return self.descripcion
