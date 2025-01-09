from django.urls import path
from .views import TipoDocumentoListView, TipoDocumentoCreateView, TipoDocumentoUpdateView, TipoDocumentoDeleteView

urlpatterns = [
    path('abm/tipodocumentos/', TipoDocumentoListView.as_view(), name='tipodocumento_list'),
    path('abm/tipodocumentos/nuevo/', TipoDocumentoCreateView.as_view(), name='tipodocumento_create'),
    path('abm/tipodocumentos/<int:pk>/editar/', TipoDocumentoUpdateView.as_view(), name='tipodocumento_update'),
    path('abm/tipodocumentos/<int:pk>/eliminar/', TipoDocumentoDeleteView.as_view(), name='tipodocumento_delete'),
]
