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
    
class Departamento(models.Model):  # Nueva tabla
    descripcion = models.TextField()

    def __str__(self):
        return self.descripcion



class TipoCliente(models.Model):
    descripcion = models.TextField()

    def __str__(self):
        return self.descripcion
    
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
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)  # Relación con Provincia

    def __str__(self):
        return self.descripcion

    
class Cliente(AuditModel):
    descripcion = models.TextField()
    fantasia = models.TextField(null=True, blank=True)
    cat_arca = models.ForeignKey(CategoriaArca, on_delete=models.SET_NULL, null=True, blank=True)
    tipo_doc = models.ForeignKey(TipoDocumento, on_delete=models.SET_NULL, null=True, blank=True)
    nro_doc = models.TextField()
    direccion = models.TextField()
    localidad = models.ForeignKey(Localidad, on_delete=models.SET_NULL, null=True, blank=True)
    rubro = models.ForeignKey(Rubro, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.descripcion
    
    def get_principal(self):
        return self.tipos.filter(principal=True).first()
    
    def get_tipo_principal(self):
        tipo_principal = self.tipos.filter(principal=True).first()
        return tipo_principal.tipo_cliente.descripcion if tipo_principal else "N/A"
    
class ClienteTipo(AuditModel):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="tipos")
    tipo_cliente = models.ForeignKey(TipoCliente, on_delete=models.CASCADE)
    principal = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Validar que solo haya un tipo principal por cliente
        if self.principal:
            ClienteTipo.objects.filter(cliente=self.cliente, principal=True).update(principal=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cliente} - {self.tipo_cliente}"


class Contacto(AuditModel):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True)  # FK a Departamento
    nombre_y_apellido = models.TextField()
    telefono = models.TextField()
    email = models.TextField()

    def __str__(self):
        return self.nombre_y_apellido
