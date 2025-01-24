from django.db import models
from utils.audit import AuditModel  # Importa el modelo base desde utils
from stock.models import Deposito, Pasillo, Columna, Estante
from clientes.models import Rubro

# Modelo para Productos
class Producto(AuditModel):
    barcode = models.TextField(null=True, blank=True, unique=False)  # Código de barras
    descripcion = models.CharField(max_length=255) # Descripción del producto
    loc_dep = models.ForeignKey(Deposito, on_delete=models.SET_NULL, null=True, blank=True)  # Depósito
    loc_pas = models.ForeignKey(Pasillo, on_delete=models.SET_NULL, null=True, blank=True)  # Pasillo
    loc_col = models.ForeignKey(Columna, on_delete=models.SET_NULL, null=True, blank=True)  # Columna
    loc_est = models.ForeignKey(Estante, on_delete=models.SET_NULL, null=True, blank=True)  # Estante
    rubro = models.ForeignKey(Rubro, on_delete=models.SET_NULL, null=True, blank=True)  # Relación con Rubro

    def __str__(self):
        return self.descripcion
    
# Modelo para Marcas
class Marca(models.Model):
    descripcion = models.TextField()

    def __str__(self):
        return self.descripcion

# Modelo para Unidades
class Unidad(models.Model):
    descripcion = models.TextField()
    abreviatura = models.CharField(max_length=3)  # New field for abbreviation

    def __str__(self):
        return f"{self.descripcion} ({self.abreviatura})" if self.abreviatura else self.descripcion


class Sinonimo(models.Model):
    descripcion = models.TextField()
    idtipo1 = models.ForeignKey('IDTipo1', on_delete=models.CASCADE, related_name='sinonimos')  # Relación uno a muchos

    def __str__(self):
        return self.descripcion


class IDTipo1(models.Model):
    descripcion = models.TextField()
    IDtipo2 = models.TextField()
    atributo1 = models.TextField(null=True, blank=True)
    atributo2 = models.TextField(null=True, blank=True)
    atributo3 = models.TextField(null=True, blank=True)
    atributo4 = models.TextField(null=True, blank=True)
    atributo5 = models.TextField(null=True, blank=True)
    pre1 = models.TextField(null=True, blank=True)
    pre2 = models.TextField(null=True, blank=True)
    pre3 = models.TextField(null=True, blank=True)
    pre4 = models.TextField(null=True, blank=True)
    pre5 = models.TextField(null=True, blank=True)
    suf1 = models.TextField(null=True, blank=True)
    suf2 = models.TextField(null=True, blank=True)
    suf3 = models.TextField(null=True, blank=True)
    suf4 = models.TextField(null=True, blank=True)
    suf5 = models.TextField(null=True, blank=True)
    cod_alpha = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return self.descripcion


# Modelo para IDTipo2
class IDTipo2(models.Model):
    descripcion = models.TextField()
    IDtipo1 = models.ForeignKey(IDTipo1, on_delete=models.CASCADE, related_name='IDTIPO2')
    cod_alpha = models.CharField(max_length=3, unique=True)  # Cambiado a CharField

    def __str__(self):
        return f"{self.IDtipo1.descripcion}: {self.descripcion}"



# Modelo para DesConcatenada
class DesConcatenada(models.Model):
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    IDtipo1 = models.ForeignKey(IDTipo1, on_delete=models.CASCADE)
    IDtipo2 = models.ForeignKey(IDTipo2, on_delete=models.CASCADE)
    atributo1 = models.TextField(null=True, blank=True)
    atributo2 = models.TextField(null=True, blank=True)
    atributo3 = models.TextField(null=True, blank=True)
    atributo4 = models.TextField(null=True, blank=True)
    atributo5 = models.TextField(null=True, blank=True)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE)
    cod_alpha = models.CharField(max_length=13, unique=True)  # Cambiado a CharField

    def save(self, *args, **kwargs):
        if not self.cod_alpha:
            idtipo1_alpha = self.IDtipo1.cod_alpha if self.IDtipo1 else ''
            idtipo2_alpha = self.IDtipo2.cod_alpha if self.IDtipo2 else ''
            producto_id_padded = str(self.producto.id).zfill(7)
            self.cod_alpha = f"{idtipo1_alpha}{idtipo2_alpha}{producto_id_padded}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.producto} - {self.IDtipo1} - {self.IDtipo2}"
