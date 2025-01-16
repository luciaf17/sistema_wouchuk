from django.db import models
from utils.audit import AuditModel  # Importa el modelo base desde utils
from stock.models import Deposito, Pasillo, Columna, Estante

# Modelo para Productos
class Producto(AuditModel):
    barcode = models.TextField(null=True, blank=True, unique=False)  # Código de barras
    descripcion = models.CharField(max_length=255) # Descripción del producto
    loc_dep = models.ForeignKey(Deposito, on_delete=models.SET_NULL, null=True, blank=True)  # Depósito
    loc_pas = models.ForeignKey(Pasillo, on_delete=models.SET_NULL, null=True, blank=True)  # Pasillo
    loc_col = models.ForeignKey(Columna, on_delete=models.SET_NULL, null=True, blank=True)  # Columna
    loc_est = models.ForeignKey(Estante, on_delete=models.SET_NULL, null=True, blank=True)  # Estante

    def __str__(self):
        return self.descripcion
