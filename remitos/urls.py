from django.urls import path
from .views import RemitoListView, RemitoCreateView, RemitoUpdateView, remito_anular, remito_activar

urlpatterns = [
    path('remitos/', RemitoListView.as_view(), name='remito_list'),
    path('remitos/create/', RemitoCreateView.as_view(), name='remito_create'),
    path('remitos/<int:pk>/update/', RemitoUpdateView.as_view(), name='remito_update'),
    path('remitos/<int:pk>/anular/', remito_anular, name='remito_anular'),
    path('remitos/<int:pk>/activar/', remito_activar, name='remito_activar'),
]
