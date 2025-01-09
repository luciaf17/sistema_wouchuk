from django.contrib import admin
from .models import Deposito, Pasillo, Columna, Estante, Stock

# Registro de los modelos
admin.site.register(Deposito)
admin.site.register(Pasillo)
admin.site.register(Columna)
admin.site.register(Estante)
admin.site.register(Stock)
