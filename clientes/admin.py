from django.contrib import admin
from .models import Cliente, Contacto, TipoDocumento, CategoriaArca, Rubro, TipoCliente, ClienteTipo


# Registro de los modelos
admin.site.register(Cliente)
admin.site.register(Contacto)
admin.site.register(TipoDocumento)
admin.site.register(CategoriaArca)
admin.site.register(Rubro)
admin.site.register(TipoCliente)
admin.site.register(ClienteTipo)
