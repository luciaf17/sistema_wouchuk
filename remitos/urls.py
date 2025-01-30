from django.urls import path
from .views import RemitoListView, RemitoCreateView, RemitoDetailView, RemitoUpdateView, remito_anular, remito_activar, ConversionMonedaListView, ConversionMonedaCreateView, ConversionMonedaUpdateView, ConversionMonedaDeleteView

urlpatterns = [
    path('remitos/', RemitoListView.as_view(), name='remito_list'),
    path('remitos/create/', RemitoCreateView.as_view(), name='remito_create'),
    path('remitos/<int:pk>/update/', RemitoUpdateView.as_view(), name='remito_update'),
    path('remitos/<int:pk>/anular/', remito_anular, name='remito_anular'),
    path('remitos/<int:pk>/activar/', remito_activar, name='remito_activar'),

    path('conversion/', ConversionMonedaListView.as_view(), name='conversion_moneda_list'),
    path('conversion/nuevo/', ConversionMonedaCreateView.as_view(), name='conversion_moneda_create'),
    path('conversion/<int:pk>/editar/', ConversionMonedaUpdateView.as_view(), name='conversion_moneda_update'),
    path('conversion/<int:pk>/eliminar/', ConversionMonedaDeleteView.as_view(), name='conversion_moneda_delete'),
    path('remitos/<int:pk>/detail/', RemitoDetailView.as_view(), name='remito_detail'),
]
