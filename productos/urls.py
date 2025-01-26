from django.urls import path
from .views import (
    ProductoListView, ProductoCreateView, ProductoUpdateView, ProductoDeleteView, buscar_google, buscar_producto,	
    MarcaListView, MarcaCreateView, MarcaUpdateView, MarcaDeleteView,
    UnidadListView, UnidadCreateView, UnidadUpdateView, UnidadDeleteView,
    SinonimoListView, SinonimoCreateView, SinonimoUpdateView, SinonimoDeleteView, sinonimo_autocomplete,
    IDTipo1ListView, IDTipo1CreateView, IDTipo1UpdateView, IDTipo1DeleteView, idtipo1_detail,
    IDTipo2ListView, IDTipo2CreateView, IDTipo2UpdateView, IDTipo2DeleteView,idtipo2_list, atributos_list,
    DesConcatenadaListView, DesConcatenadaCreateView, DesConcatenadaUpdateView, atributo_autocomplete, calcular_cod_alpha,
    TipoIDTipo2ListView,
    TipoIDTipo2CreateView,
    TipoIDTipo2UpdateView,
    TipoIDTipo2DeleteView, get_idtipo1_details
)

urlpatterns = [
    path('productos/', ProductoListView.as_view(), name='producto_list'),
    path('productos/create/', ProductoCreateView.as_view(), name='producto_create'),
    path('productos/<int:pk>/update/', ProductoUpdateView.as_view(), name='producto_update'),
    path('productos/<int:pk>/delete/', ProductoDeleteView.as_view(), name='producto_delete'),
    path('buscar-google/', buscar_google, name='buscar_google'),
    path('buscar/', buscar_producto, name='buscar_producto'),

     # URLs para Marcas
    path('marcas/', MarcaListView.as_view(), name='marca_list'),
    path('marcas/create/', MarcaCreateView.as_view(), name='marca_create'),
    path('marcas/<int:pk>/update/', MarcaUpdateView.as_view(), name='marca_update'),
    path('marcas/<int:pk>/delete/', MarcaDeleteView.as_view(), name='marca_delete'),

    # URLs para Unidades
    path('unidades/', UnidadListView.as_view(), name='unidad_list'),
    path('unidades/create/', UnidadCreateView.as_view(), name='unidad_create'),
    path('unidades/<int:pk>/update/', UnidadUpdateView.as_view(), name='unidad_update'),
    path('unidades/<int:pk>/delete/', UnidadDeleteView.as_view(), name='unidad_delete'),

    # URLs para Sinónimos
    path('sinonimos/', SinonimoListView.as_view(), name='sinonimo_list'),
    path('sinonimos/create/', SinonimoCreateView.as_view(), name='sinonimo_create'),
    path('sinonimos/<int:pk>/update/', SinonimoUpdateView.as_view(), name='sinonimo_update'),
    path('sinonimos/<int:pk>/delete/', SinonimoDeleteView.as_view(), name='sinonimo_delete'),

    path('idtipo1/', IDTipo1ListView.as_view(), name='idtipo1_list'),
    path('idtipo1/create/', IDTipo1CreateView.as_view(), name='idtipo1_create'),
    path('idtipo1/<int:pk>/update/', IDTipo1UpdateView.as_view(), name='idtipo1_update'),
    path('idtipo1/<int:pk>/delete/', IDTipo1DeleteView.as_view(), name='idtipo1_delete'),
    path('sinonimos/autocomplete/', sinonimo_autocomplete, name='sinonimo_autocomplete'),
    path('idtipo1/<int:idtipo1_id>/', idtipo1_detail, name='idtipo1_detail'),

    path('idtipo2/', IDTipo2ListView.as_view(), name='idtipo2_list'),
    path('idtipo2/crear/', IDTipo2CreateView.as_view(), name='idtipo2_create'),
    path('idtipo2/editar/<int:pk>/', IDTipo2UpdateView.as_view(), name='idtipo2_update'),
    path('idtipo2/eliminar/<int:pk>/', IDTipo2DeleteView.as_view(), name='idtipo2_delete'),
    path('idtipo2/<int:idtipo1_id>/', idtipo2_list, name='idtipo2_list'),
    path('atributos/<int:idtipo1_id>/', atributos_list, name='atributos_list'),

    path('productos/desconcatenada/<int:producto_id>/', DesConcatenadaListView.as_view(), name='desconcatenada_list'),
    path('productos/desconcatenada/<int:producto_id>/crear/', DesConcatenadaCreateView.as_view(), name='desconcatenada_create'),
    path('productos/desconcatenada/editar/<int:pk>/', DesConcatenadaUpdateView.as_view(), name='desconcatenada_update'),
    path('atributo-autocomplete/', atributo_autocomplete, name='atributo_autocomplete'),
    path('calcular_cod_alpha/', calcular_cod_alpha, name='calcular_cod_alpha'),

    path('tipoidtipo2/', TipoIDTipo2ListView.as_view(), name='tipoidtipo2_list'),
    path('tipoidtipo2/nuevo/', TipoIDTipo2CreateView.as_view(), name='tipoidtipo2_create'),
    path('tipoidtipo2/<int:pk>/editar/', TipoIDTipo2UpdateView.as_view(), name='tipoidtipo2_update'),
    path('tipoidtipo2/<int:pk>/eliminar/', TipoIDTipo2DeleteView.as_view(), name='tipoidtipo2_delete'),
    path('idtipo1/<int:idTipo1>/', get_idtipo1_details, name='get_idtipo1_details'),

]
