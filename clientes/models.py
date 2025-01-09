from django.db import models

# Tipo de Documento: ENUM que define diferentes tipos de documento (ej. DNI, CUIT)
class TipoDocumento(models.Model):
    descripcion = models.TextField()  # Nombre del tipo de documento

    def __str__(self):
        return self.descripcion


# Categoría Aranca: ENUM que clasifica las categorías arancelarias
class CategoriaArca(models.Model):
    descripcion = models.TextField()  # Descripción de la categoría arancelaria

    def __str__(self):
        return self.descripcion


# Rubro: ENUM que clasifica los rubros de los clientes
class Rubro(models.Model):
    descripcion = models.TextField()  # Descripción del rubro

    def __str__(self):
        return self.descripcion


# Modelo principal de Clientes
class Cliente(models.Model):
    descripcion = models.TextField()  # Nombre o razón social del cliente
    fantasia = models.TextField(null=True, blank=True)  # Nombre de fantasía del cliente (antes abreviatura)
    cat_arca = models.ForeignKey(CategoriaArca, on_delete=models.SET_NULL, null=True, blank=True)  # Categoría arancelaria
    tipo_doc = models.ForeignKey('TipoDocumento', on_delete=models.SET_NULL, null=True, blank=True)  # Tipo de documento
    nro_doc = models.TextField()  # Número de documento del cliente
    direccion = models.TextField()  # Dirección del cliente
    localidad = models.ForeignKey('remitos.Localidad', on_delete=models.SET_NULL, null=True, blank=True)  # Localidad
    rubro = models.ForeignKey('Rubro', on_delete=models.SET_NULL, null=True, blank=True)  # Rubro del cliente

    def __str__(self):
        return self.descripcion


# Tipos de Cliente: ENUM que clasifica los diferentes tipos de cliente (ej. Proveedor, Transporte)
class TipoCliente(models.Model):
    descripcion = models.TextField()  # Descripción del tipo de cliente

    def __str__(self):
        return self.descripcion


# Relación entre Clientes y Tipos de Cliente
class ClienteTipo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # Cliente relacionado
    tipo_cliente = models.ForeignKey(TipoCliente, on_delete=models.CASCADE)  # Tipo de cliente relacionado
    principal = models.BooleanField(default=False)  # Indica si es el tipo principal

    def __str__(self):
        return f"{self.cliente} - {self.tipo_cliente}"


# Contactos: Define los contactos relacionados a cada cliente
class Contacto(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # Cliente al que pertenece este contacto
    departamento = models.TextField(null=True, blank=True)  # Departamento del contacto
    nombre_y_apellido = models.TextField()  # Nombre completo del contacto
    telefono = models.TextField()  # Teléfono del contacto
    email = models.TextField()  # Correo electrónico del contacto

    def __str__(self):
        return self.nombre_y_apellido
