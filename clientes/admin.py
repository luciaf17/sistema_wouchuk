from django.contrib import admin
from .models import Cliente, Contacto, TipoDocumento, CategoriaArca, Rubro, TipoCliente, ClienteTipo


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'fantasia', 'nro_doc', 'created_at', 'updated_at', 'created_by', 'updated_by')
    list_filter = ('created_at', 'updated_at', 'created_by', 'updated_by')
    search_fields = ('descripcion', 'fantasia', 'nro_doc')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')  # Campos de solo lectura


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre_y_apellido', 'cliente', 'telefono', 'email', 'created_at', 'updated_at', 'created_by', 'updated_by')
    list_filter = ('created_at', 'updated_at', 'created_by', 'updated_by')
    search_fields = ('nombre_y_apellido', 'cliente__descripcion', 'email')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')  # Campos de solo lectura


@admin.register(ClienteTipo)
class ClienteTipoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'tipo_cliente', 'principal', 'created_at', 'updated_at', 'created_by', 'updated_by')
    list_filter = ('tipo_cliente', 'created_at', 'updated_at', 'created_by', 'updated_by')
    search_fields = ('cliente__descripcion', 'tipo_cliente__descripcion')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')  # Campos de solo lectura


# Registro básico para los modelos que no necesitan personalización
admin.site.register(TipoDocumento)
admin.site.register(CategoriaArca)
admin.site.register(Rubro)
admin.site.register(TipoCliente)
