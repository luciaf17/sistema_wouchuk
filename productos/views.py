from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from stock.models import Deposito, Pasillo, Columna, Estante
from .models import Producto
from .forms import ProductoForm
from django.db import models
import requests
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def buscar_producto(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        query = data.get('query', '').strip()

        if query:
            # Dividir la consulta en palabras individuales
            palabras = query.split()

            # Crear un filtro Q dinámico para buscar cada palabra
            q_filter = models.Q()
            for palabra in palabras:
                q_filter &= models.Q(descripcion__icontains=palabra) | models.Q(barcode__icontains=palabra)

            # Filtra productos utilizando el filtro compuesto
            productos = Producto.objects.filter(q_filter) # Limitar resultados a 10 para evitar sobrecarga

            # Incluye el `id` de los productos en el resultado
            resultado = [
                {'id': p.id, 'barcode': p.barcode, 'descripcion': p.descripcion}
                for p in productos
            ]
            return JsonResponse({'productos': resultado})

        return JsonResponse({'productos': []})
    return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
def buscar_google(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        barcode = data.get('barcode', None)
        if barcode:
            descripcion = obtener_datos_de_google(barcode)
            return JsonResponse({'descripcion': descripcion})
        return JsonResponse({'error': 'Código de barras no proporcionado'}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def obtener_datos_de_google(codigo):
    api_key = "AIzaSyCj_8KdMBBWdlCZwZUD59LbuXC0m-Qkbis"  # Reemplaza con tu clave
    search_engine_id = "c2fe79724f3994723"  # Reemplaza con tu ID
    url = f"https://www.googleapis.com/customsearch/v1?q={codigo}&key={api_key}&cx={search_engine_id}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "items" in data and len(data["items"]) > 0:
            titulo = data["items"][0]["title"]
            titulo_texto = re.split(r' - | \(|\[|\{', titulo)[0].strip()
            return titulo_texto.capitalize()
        else:
            return "Artículo no encontrado"
    else:
        return "Error en la búsqueda"

from django.db.models import Q

class ProductoListView(ListView):
    model = Producto
    template_name = 'productos/producto_list.html'
    context_object_name = 'productos'

    def get_queryset(self):
        queryset = Producto.objects.all()

        # Obtener los parámetros de búsqueda
        query = self.request.GET.get('q', '').strip()
        loc_dep = self.request.GET.get('loc_dep', '')
        loc_pas = self.request.GET.get('loc_pas', '')
        loc_col = self.request.GET.get('loc_col', '')
        loc_est = self.request.GET.get('loc_est', '')

        # Filtrar por descripción o código de barras (búsqueda avanzada)
        if query:
            palabras = query.split()
            q_filter = Q()
            for palabra in palabras:
                q_filter &= Q(descripcion__icontains=palabra) | Q(barcode__icontains=palabra)
            queryset = queryset.filter(q_filter)

        # Filtrar por depósito
        if loc_dep:
            queryset = queryset.filter(loc_dep_id=loc_dep)

        # Filtrar por pasillo
        if loc_pas:
            queryset = queryset.filter(loc_pas_id=loc_pas)

        # Filtrar por columna
        if loc_col:
            queryset = queryset.filter(loc_col_id=loc_col)

        # Filtrar por estante
        if loc_est:
            queryset = queryset.filter(loc_est_id=loc_est)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregar datos de los select para filtros al contexto
        context['depositos'] = Deposito.objects.all()
        context['pasillos'] = Pasillo.objects.all()
        context['columnas'] = Columna.objects.all()
        context['estantes'] = Estante.objects.all()
        return context


class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/producto_form.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['loc_dep'] = 1
        initial['loc_pas'] = 1
        initial['loc_col'] = 1
        initial['loc_est'] = 1
        return initial

    def form_invalid(self, form):
        # Maneja errores de validación, como códigos de barras duplicados
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        # Si no hay descripción y el código de barras está presente, buscar en Google
        if not form.cleaned_data['descripcion'] and form.cleaned_data['barcode']:
            codigo = form.cleaned_data['barcode']
            descripcion = obtener_datos_de_google(codigo)
            form.instance.descripcion = descripcion
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('producto_list')

class ProductoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/producto_form.html'

    def get_success_url(self):
        return reverse_lazy('producto_list')

class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('producto_list')
