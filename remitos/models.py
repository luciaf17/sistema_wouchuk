from django.db import models
from utils.audit import AuditModel  # Importa el modelo base desde utils

# Modelo para Paises
class Pais(models.Model):
    descripcion = models.TextField()  # Nombre del país
    cod_tel = models.TextField(null=True, blank=True)  # Código telefónico
    gtm = models.TextField(null=True, blank=True)  # Zona horaria

    def __str__(self):
        return self.descripcion


# Modelo para Provincias
class Provincia(models.Model):
    descripcion = models.TextField()  # Nombre de la provincia
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)  # Relación con Pais

    def __str__(self):
        return self.descripcion


# Modelo para Localidades
class Localidad(models.Model):
    descripcion = models.TextField()  # Nombre de la localidad
    cp = models.TextField()  # Código postal
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)  # Relación con Pais
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)  # Relación con Provincia

    def __str__(self):
        return self.descripcion


# Tipos de Remitos: ENUM que clasifica los remitos (ej. Compra, Venta)
class TipoRemito(models.Model):
    descripcion = models.TextField()

    def __str__(self):
        return self.descripcion


# Estados de Remitos: ENUM que clasifica los estados (ej. Abierto, Cerrado)
class EstadoRemito(AuditModel):
    descripcion = models.TextField()

    def __str__(self):
        return self.descripcion


# Modelo principal de Remitos
class Remito(AuditModel):
    tipo_remito = models.ForeignKey(TipoRemito, on_delete=models.SET_NULL, null=True, blank=True)  # Tipo de remito
    cliente = models.ForeignKey('clientes.Cliente', on_delete=models.SET_NULL, null=True, blank=True)  # Cliente relacionado
    dep_origen = models.ForeignKey('stock.Deposito', on_delete=models.SET_NULL, null=True, blank=True, related_name='remitos_origen')  # Depósito origen
    dep_destino = models.ForeignKey('stock.Deposito', on_delete=models.SET_NULL, null=True, blank=True, related_name='remitos_destino')  # Depósito destino
    nro_comprobante_asoc = models.TextField(null=True, blank=True)  # Número de comprobante asociado
    fecha = models.DateTimeField(auto_now_add=True)  # Fecha del remito
    estado_remito = models.ForeignKey(EstadoRemito, on_delete=models.SET_NULL, null=True, blank=True)  # Estado del remito

    def __str__(self):
        return f"{self.tipo_remito} - {self.fecha}"


# Detalles del Remito: Define los productos asociados a un remito
class DetalleRemito(AuditModel):
    remito = models.ForeignKey(Remito, on_delete=models.CASCADE)  # Remito relacionado
    producto = models.ForeignKey('productos.Producto', on_delete=models.CASCADE)  # Producto relacionado
    cantidad = models.PositiveIntegerField()  # Cantidad de producto en el remito
    precio_unit = models.DecimalField(max_digits=10, decimal_places=2)  # Precio unitario

    def __str__(self):
        return f"{self.remito} - {self.producto} - {self.cantidad}"
