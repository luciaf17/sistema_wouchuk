# urls.py
from django.urls import path
from .views import (DepositoListView, DepositoCreateView, DepositoUpdateView, DepositoDeleteView, ConsultaStockView,
                    PasilloListView, PasilloCreateView, PasilloUpdateView, PasilloDeleteView,
                    ColumnaListView, ColumnaCreateView, ColumnaUpdateView, ColumnaDeleteView,
                    EstanteListView, EstanteCreateView, EstanteUpdateView, EstanteDeleteView,)

urlpatterns = [

    # Consulta de Stock
    path('consulta/', ConsultaStockView.as_view(), name='consulta_stock'),

    # Depósitos
    path('depositos/', DepositoListView.as_view(), name='deposito_list'),
    path('depositos/create/', DepositoCreateView.as_view(), name='deposito_create'),
    path('depositos/<int:pk>/update/', DepositoUpdateView.as_view(), name='deposito_update'),
    path('depositos/<int:pk>/delete/', DepositoDeleteView.as_view(), name='deposito_delete'),

    # Pasillo
    path('pasillos/', PasilloListView.as_view(), name='pasillo_list'),
    path('pasillos/create/', PasilloCreateView.as_view(), name='pasillo_create'),
    path('pasillos/<int:pk>/update/', PasilloUpdateView.as_view(), name='pasillo_update'),
    path('pasillos/<int:pk>/delete/', PasilloDeleteView.as_view(), name='pasillo_delete'),

    # Columna
    path('columnas/', ColumnaListView.as_view(), name='columna_list'),
    path('columnas/create/', ColumnaCreateView.as_view(), name='columna_create'),
    path('columnas/<int:pk>/update/', ColumnaUpdateView.as_view(), name='columna_update'),
    path('columnas/<int:pk>/delete/', ColumnaDeleteView.as_view(), name='columna_delete'),

    # Estante
    path('estantes/', EstanteListView.as_view(), name='estante_list'),
    path('estantes/create/', EstanteCreateView.as_view(), name='estante_create'),
    path('estantes/<int:pk>/update/', EstanteUpdateView.as_view(), name='estante_update'),
    path('estantes/<int:pk>/delete/', EstanteDeleteView.as_view(), name='estante_delete'),
]
