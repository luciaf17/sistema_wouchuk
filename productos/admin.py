from django.contrib import admin
from .models import Producto, Marca, Unidad, Sinonimo

# Registro del modelo Producto
admin.site.register(Producto)
admin.site.register(Marca)
admin.site.register(Unidad)
admin.site.register(Sinonimo)
