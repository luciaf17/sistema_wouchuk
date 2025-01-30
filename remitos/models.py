from django.db import models
from utils.audit import AuditModel
from stock.models import Deposito
from clientes.models import Cliente


class Remito(AuditModel):
    tipo_remito = models.CharField(max_length=50, choices=[
        ('ajuste', 'Ajuste'),
        ('compra', 'Compra'),
        ('venta', 'Venta'),
        ('interdeposito', 'Interdepósito'),
    ])
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    nro_comprobante_asoc = models.TextField(null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    estado_remito = models.CharField(max_length=50, choices=[
        ('activo', 'Activo'),
        ('anulado', 'Anulado'),
    ], default='activo')

    def __str__(self):
        return f"{self.tipo_remito} - {self.fecha}"


class DetalleRemito(AuditModel):
    remito = models.ForeignKey(Remito, on_delete=models.CASCADE, verbose_name="Remito")
    producto = models.ForeignKey('productos.Producto', on_delete=models.CASCADE, verbose_name="Producto")
    dep_origen = models.ForeignKey(Deposito, on_delete=models.SET_NULL, null=True, blank=True, related_name='detalles_origen')
    dep_destino = models.ForeignKey(Deposito, on_delete=models.SET_NULL, null=True, blank=True, related_name='detalles_destino')
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad")
    moneda = models.ForeignKey('ConversionMoneda', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Moneda")
    precio_unit = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Unitario")

    def __str__(self):
        return f"{self.remito} - {self.producto} - {self.cantidad}"
    
class ConversionMoneda(models.Model):
    moneda = models.CharField(max_length=50, unique=True, verbose_name="Moneda")
    simbolo = models.CharField(max_length=10, unique=True, verbose_name="Símbolo")
    conversion = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor de Conversión")

    def __str__(self):
        return f"{self.moneda} ({self.simbolo}) - {self.conversion}"
