from django.db import models
from utils.audit import AuditModel  # Importa el modelo base desde utils


class TipoDocumento(AuditModel):
    descripcion = models.TextField()

    def __str__(self):
        return self.descripcion


class CategoriaArca(models.Model):
    descripcion = models.TextField()

    def __str__(self):
        return self.descripcion


class Rubro(models.Model):
    descripcion = models.TextField()

    def __str__(self):
        return self.descripcion


class Cliente(AuditModel):
    descripcion = models.TextField()
    fantasia = models.TextField(null=True, blank=True)
    cat_arca = models.ForeignKey(CategoriaArca, on_delete=models.SET_NULL, null=True, blank=True)
    tipo_doc = models.ForeignKey(TipoDocumento, on_delete=models.SET_NULL, null=True, blank=True)
    nro_doc = models.TextField()
    direccion = models.TextField()
    localidad = models.ForeignKey('remitos.Localidad', on_delete=models.SET_NULL, null=True, blank=True)
    rubro = models.ForeignKey(Rubro, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.descripcion


class TipoCliente(models.Model):
    descripcion = models.TextField()

    def __str__(self):
        return self.descripcion


class ClienteTipo(AuditModel):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tipo_cliente = models.ForeignKey(TipoCliente, on_delete=models.CASCADE)
    principal = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.cliente} - {self.tipo_cliente}"


class Contacto(AuditModel):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    departamento = models.TextField(null=True, blank=True)
    nombre_y_apellido = models.TextField()
    telefono = models.TextField()
    email = models.TextField()

    def __str__(self):
        return self.nombre_y_apellido
