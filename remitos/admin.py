from django.contrib import admin
from .models import Pais, Provincia, Localidad, TipoRemito, EstadoRemito, Remito, DetalleRemito

# Registro de los modelos
admin.site.register(Pais)
admin.site.register(Provincia)
admin.site.register(Localidad)
admin.site.register(TipoRemito)
admin.site.register(EstadoRemito)
admin.site.register(Remito)
admin.site.register(DetalleRemito)
