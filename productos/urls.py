from django.urls import path
from .views import ProductoListView, ProductoCreateView, ProductoUpdateView, ProductoDeleteView, buscar_google, buscar_producto

urlpatterns = [
    path('productos/', ProductoListView.as_view(), name='producto_list'),
    path('productos/create/', ProductoCreateView.as_view(), name='producto_create'),
    path('productos/<int:pk>/update/', ProductoUpdateView.as_view(), name='producto_update'),
    path('productos/<int:pk>/delete/', ProductoDeleteView.as_view(), name='producto_delete'),
    path('buscar-google/', buscar_google, name='buscar_google'),
    path('buscar/', buscar_producto, name='buscar_producto'),
]
