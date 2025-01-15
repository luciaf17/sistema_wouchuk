from django.contrib import admin
from .models import TipoRemito, EstadoRemito, Remito, DetalleRemito

# Registro de los modelos
admin.site.register(TipoRemito)
admin.site.register(EstadoRemito)
admin.site.register(Remito)
admin.site.register(DetalleRemito)
