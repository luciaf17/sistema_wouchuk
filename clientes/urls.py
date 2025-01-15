from django.urls import path
from .views import (TipoDocumentoListView, TipoDocumentoCreateView, TipoDocumentoUpdateView, TipoDocumentoDeleteView, 
                    CategoriaArcaListView, CategoriaArcaCreateView, CategoriaArcaUpdateView, CategoriaArcaDeleteView,
                    RubroListView, RubroCreateView, RubroUpdateView, RubroDeleteView,
                    DepartamentoListView, DepartamentoCreateView, DepartamentoUpdateView, DepartamentoDeleteView,
                    TipoClienteListView, TipoClienteCreateView, TipoClienteUpdateView, TipoClienteDeleteView,
                    PaisListView, PaisCreateView, PaisUpdateView, PaisDeleteView,
                    ProvinciaListView, ProvinciaCreateView, ProvinciaUpdateView, ProvinciaDeleteView,
                    LocalidadListView, LocalidadCreateView, LocalidadUpdateView, LocalidadDeleteView,
                    ClienteListView, ClienteCreateView, ClienteUpdateView, ClienteDeleteView,
                    ClienteTipoCreateView, ClienteTipoDeleteView,
                    ContactoCreateView, ContactoListView, ContactoUpdateView, ContactoDeleteView


)

urlpatterns = [
    path('abm/tipodocumentos/', TipoDocumentoListView.as_view(), name='tipodocumento_list'),
    path('abm/tipodocumentos/nuevo/', TipoDocumentoCreateView.as_view(), name='tipodocumento_create'),
    path('abm/tipodocumentos/<int:pk>/editar/', TipoDocumentoUpdateView.as_view(), name='tipodocumento_update'),
    path('abm/tipodocumentos/<int:pk>/eliminar/', TipoDocumentoDeleteView.as_view(), name='tipodocumento_delete'),
    
    path('categoriaarca/', CategoriaArcaListView.as_view(), name='categoriaarca_list'),
    path('categoriaarca/nuevo/', CategoriaArcaCreateView.as_view(), name='categoriaarca_create'),
    path('categoriaarca/<int:pk>/editar/', CategoriaArcaUpdateView.as_view(), name='categoriaarca_update'),
    path('categoriaarca/<int:pk>/eliminar/', CategoriaArcaDeleteView.as_view(), name='categoriaarca_delete'),

    path('rubros/', RubroListView.as_view(), name='rubro_list'),
    path('rubros/crear/', RubroCreateView.as_view(), name='rubro_create'),
    path('rubros/editar/<int:pk>/', RubroUpdateView.as_view(), name='rubro_update'),
    path('rubros/eliminar/<int:pk>/', RubroDeleteView.as_view(), name='rubro_delete'),

    path('departamentos/', DepartamentoListView.as_view(), name='departamento_list'),
    path('departamentos/crear/', DepartamentoCreateView.as_view(), name='departamento_create'),
    path('departamentos/editar/<int:pk>/', DepartamentoUpdateView.as_view(), name='departamento_update'),
    path('departamentos/eliminar/<int:pk>/', DepartamentoDeleteView.as_view(), name='departamento_delete'),

    path('tipoclientes/', TipoClienteListView.as_view(), name='tipocliente_list'),
    path('tipoclientes/crear/', TipoClienteCreateView.as_view(), name='tipocliente_create'),
    path('tipoclientes/editar/<int:pk>/', TipoClienteUpdateView.as_view(), name='tipocliente_update'),
    path('tipoclientes/eliminar/<int:pk>/', TipoClienteDeleteView.as_view(), name='tipocliente_delete'),

    path('paises/', PaisListView.as_view(), name='pais_list'),
    path('paises/crear/', PaisCreateView.as_view(), name='pais_create'),
    path('paises/editar/<int:pk>/', PaisUpdateView.as_view(), name='pais_update'),
    path('paises/eliminar/<int:pk>/', PaisDeleteView.as_view(), name='pais_delete'),

    path('provincias/', ProvinciaListView.as_view(), name='provincia_list'),
    path('provincias/crear/', ProvinciaCreateView.as_view(), name='provincia_create'),
    path('provincias/editar/<int:pk>/', ProvinciaUpdateView.as_view(), name='provincia_update'),
    path('provincias/eliminar/<int:pk>/', ProvinciaDeleteView.as_view(), name='provincia_delete'),

    path('localidades/', LocalidadListView.as_view(), name='localidad_list'),
    path('localidades/crear/', LocalidadCreateView.as_view(), name='localidad_create'),
    path('localidades/editar/<int:pk>/', LocalidadUpdateView.as_view(), name='localidad_update'),
    path('localidades/eliminar/<int:pk>/', LocalidadDeleteView.as_view(), name='localidad_delete'),

     # Cliente
    path('clientes/', ClienteListView.as_view(), name='cliente_list'),
    path('clientes/create/', ClienteCreateView.as_view(), name='cliente_create'),
    path('clientes/<int:pk>/update/', ClienteUpdateView.as_view(), name='cliente_update'),
    path('clientes/<int:pk>/delete/', ClienteDeleteView.as_view(), name='cliente_delete'),

    # ClienteTipo
    path('clientetipos/create/', ClienteTipoCreateView.as_view(), name='clientetipo_create'),
    path('clientes/tipos/delete/<int:pk>/', ClienteTipoDeleteView.as_view(), name='cliente_tipo_delete'),


    # Contacto
    path('contactos/<int:cliente_id>/', ContactoListView.as_view(), name='contacto_list'),
    path('contactos/<int:cliente_id>/create/', ContactoCreateView.as_view(), name='contacto_create'),
    path('contactos/<int:pk>/update/', ContactoUpdateView.as_view(), name='contacto_update'),
    path('contactos/<int:pk>/delete/', ContactoDeleteView.as_view(), name='contacto_delete'),
]
