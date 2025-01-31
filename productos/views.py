from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from stock.models import Deposito, Pasillo, Columna, Estante
from clientes.models import Rubro
from .models import Marca, Unidad, Sinonimo
from .forms import MarcaForm, UnidadForm, SinonimoForm
from .models import Producto, IDTipo1, IDTipo2, DesConcatenada, TipoIDTipo2
from .forms import ProductoForm, IDTipo1Form, IDTipo2Form, DesConcatenadaForm, TipoIDTipo2Form
from django.db import models
import requests
import re
from django.shortcuts import get_object_or_404
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

            # Incluye el `id`, `descripcion`, `barcode` y el `loc_dep` en el resultado
            resultado = [
                {
                    'id': p.id,
                    'barcode': p.barcode,
                    'descripcion': p.descripcion,
                    'loc_dep': {
                        'id': p.loc_dep.id if p.loc_dep else None,
                        'descripcion': p.loc_dep.descripcion if p.loc_dep else 'Sin Depósito'
                    }
                }
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
        rubro = self.request.GET.get('rubro', '')

        # Filtrar por descripción o código de barras (búsqueda avanzada)
        if query:
            palabras = query.split()
            q_filter = Q()
            for palabra in palabras:
                q_filter &= (Q(descripcion__icontains=palabra) | Q(barcode__icontains=palabra))
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

        # Filtrar por rubro
        if rubro:
            queryset = queryset.filter(rubro_id=rubro)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregar datos de los select para filtros al contexto
        context['depositos'] = Deposito.objects.all()
        context['pasillos'] = Pasillo.objects.all()
        context['columnas'] = Columna.objects.all()
        context['estantes'] = Estante.objects.all()
        context['rubros'] = Rubro.objects.all()  # Agregar rubros al contexto
        return context


class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/producto_form.html'


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


# Vistas para Marcas
class MarcaListView(ListView):
    model = Marca
    template_name = 'productos/marca_list.html'
    context_object_name = 'marcas'

class MarcaCreateView(CreateView):
    model = Marca
    form_class = MarcaForm
    template_name = 'productos/marca_form.html'
    success_url = reverse_lazy('marca_list')

class MarcaUpdateView(UpdateView):
    model = Marca
    form_class = MarcaForm
    template_name = 'productos/marca_form.html'
    success_url = reverse_lazy('marca_list')

class MarcaDeleteView(DeleteView):
    model = Marca
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('marca_list')

# Vistas para Unidades
class UnidadListView(ListView):
    model = Unidad
    template_name = 'productos/unidad_list.html'
    context_object_name = 'unidades'

class UnidadCreateView(CreateView):
    model = Unidad
    form_class = UnidadForm
    template_name = 'productos/unidad_form.html'
    success_url = reverse_lazy('unidad_list')

class UnidadUpdateView(UpdateView):
    model = Unidad
    form_class = UnidadForm
    template_name = 'productos/unidad_form.html'
    success_url = reverse_lazy('unidad_list')

class UnidadDeleteView(DeleteView):
    model = Unidad
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('unidad_list')

# Vistas para Sinónimos
class SinonimoListView(ListView):
    model = Sinonimo
    template_name = 'productos/sinonimo_list.html'
    context_object_name = 'sinonimos'

class SinonimoCreateView(CreateView):
    model = Sinonimo
    form_class = SinonimoForm
    template_name = 'productos/sinonimo_form.html'
    success_url = reverse_lazy('sinonimo_list')

class SinonimoUpdateView(UpdateView):
    model = Sinonimo
    form_class = SinonimoForm
    template_name = 'productos/sinonimo_form.html'
    success_url = reverse_lazy('sinonimo_list')

class SinonimoDeleteView(DeleteView):
    model = Sinonimo
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('sinonimo_list')


def sinonimo_autocomplete(request):
    term = request.GET.get('term', '')
    sinonimos = Sinonimo.objects.filter(descripcion__icontains=term).values_list('descripcion', flat=True)
    return JsonResponse(list(sinonimos), safe=False)

def atributo_autocomplete(request):
    term = request.GET.get('term', '')
    atributos = set()
    for i in range(1, 6):  # Itera por atributo1 a atributo5
        field = f"atributo{i}"
        atributos.update(
            IDTipo1.objects.filter(**{f"{field}__icontains": term}).values_list(field, flat=True)
        )
    return JsonResponse(list(atributos), safe=False)


class IDTipo1ListView(ListView):
    model = IDTipo1
    template_name = 'productos/idtipo1_list.html'
    context_object_name = 'idtipo1_list'

class IDTipo1CreateView(CreateView):
    model = IDTipo1
    form_class = IDTipo1Form
    template_name = 'productos/idtipo1_form.html'
    success_url = reverse_lazy('idtipo1_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attribute_fields'] = [
            field for field in self.get_form() if field.name.startswith('atributo')
        ]
        return context
    
    def form_valid(self, form):
        # Guarda la instancia y procesa los sinónimos
        form.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        # Redirige a la lista de IDTipo1
        return reverse_lazy('idtipo1_list')

class IDTipo1UpdateView(UpdateView):
    model = IDTipo1
    form_class = IDTipo1Form
    template_name = 'productos/idtipo1_form.html'
    success_url = reverse_lazy('idtipo1_list')

class IDTipo1DeleteView(DeleteView):
    model = IDTipo1
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('idtipo1_list')


# Listar IDTipo2
class IDTipo2ListView(ListView):
    model = IDTipo2
    template_name = 'productos/idtipo2_list.html'
    context_object_name = 'idtipo2_list'

# Crear IDTipo2
class IDTipo2CreateView(CreateView):
    model = IDTipo2
    form_class = IDTipo2Form
    template_name = 'productos/idtipo2_form.html'
    success_url = reverse_lazy('idtipo2_list')

# Editar IDTipo2
class IDTipo2UpdateView(UpdateView):
    model = IDTipo2
    form_class = IDTipo2Form
    template_name = 'productos/idtipo2_form.html'
    success_url = reverse_lazy('idtipo2_list')

# Eliminar IDTipo2
class IDTipo2DeleteView(DeleteView):
    model = IDTipo2
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('idtipo2_list')

# Listar DesConcatenada para un producto
class DesConcatenadaListView(ListView):
    model = DesConcatenada
    template_name = 'productos/desconcatenada_list.html'
    context_object_name = 'atributos'

    def get_queryset(self):
        producto_id = self.kwargs['producto_id']
        return (
            DesConcatenada.objects
            .filter(producto_id=producto_id)
            .select_related('producto', 'IDtipo1', 'IDtipo2', 'marca', 'unidad')  # Relaciones directas
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        producto = get_object_or_404(Producto, id=self.kwargs['producto_id'])
        atributos_definidos = DesConcatenada.objects.filter(producto=producto).select_related("IDtipo1").first()

        # Pasar los nombres de los atributos definidos en IDTipo1
        if atributos_definidos and atributos_definidos.IDtipo1:
            context['atributo_nombres'] = [
                atributos_definidos.IDtipo1.atributo1,
                atributos_definidos.IDtipo1.atributo2,
                atributos_definidos.IDtipo1.atributo3,
                atributos_definidos.IDtipo1.atributo4,
                atributos_definidos.IDtipo1.atributo5,
            ]
        else:
            context['atributo_nombres'] = ["Atributo 1", "Atributo 2", "Atributo 3", "Atributo 4", "Atributo 5"]

        context['producto'] = producto
        return context


# Crear DesConcatenada
class DesConcatenadaCreateView(CreateView):
    model = DesConcatenada
    form_class = DesConcatenadaForm
    template_name = 'productos/desconcatenada_form.html'

    def dispatch(self, request, *args, **kwargs):
        producto_id = self.kwargs['producto_id']
        # Verifica si ya existe un atributo para este producto
        if DesConcatenada.objects.filter(producto_id=producto_id).exists():
            atributo = DesConcatenada.objects.get(producto_id=producto_id)
            return redirect('desconcatenada_update', pk=atributo.id)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        producto = get_object_or_404(Producto, id=self.kwargs['producto_id'])
        form.instance.producto = producto
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('desconcatenada_list', kwargs={'producto_id': self.kwargs['producto_id']})
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        producto = get_object_or_404(Producto, id=self.kwargs['producto_id'])
        kwargs['producto'] = producto
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['producto'] = get_object_or_404(Producto, id=self.kwargs['producto_id'])
        return context


# Editar DesConcatenada
class DesConcatenadaUpdateView(UpdateView):
    model = DesConcatenada
    form_class = DesConcatenadaForm
    template_name = 'productos/desconcatenada_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.object  # Pasamos la instancia actual de DesConcatenada
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Contexto relacionado con el producto a través de la instancia de DesConcatenada
        context['producto'] = self.object.producto
        return context

    def get_success_url(self):
        # Redirigir a la lista de atributos relacionados con el producto
        return reverse_lazy('desconcatenada_list', kwargs={'producto_id': self.object.producto.id})



def idtipo2_list(request, idtipo1_id):
    idtipo2 = IDTipo2.objects.filter(IDtipo1_id=idtipo1_id).values('id', 'descripcion')
    return JsonResponse(list(idtipo2), safe=False)

def atributos_list(request, idtipo1_id):
    idtipo1 = get_object_or_404(IDTipo1, id=idtipo1_id)
    atributos = [
        idtipo1.atributo1, idtipo1.atributo2, idtipo1.atributo3,
        idtipo1.atributo4, idtipo1.atributo5
    ]
    return JsonResponse([attr for attr in atributos if attr], safe=False)

def idtipo1_detail(request, idtipo1_id):
    # Obtener el objeto IDTipo1 o devolver un 404 si no existe
    idtipo1 = get_object_or_404(IDTipo1, id=idtipo1_id)
    
    # Verificar si tiene un IDTipo2 asociado
    if idtipo1.IDtipo2:
        idtipo2_data = {
            'id': idtipo1.IDtipo2.id,
            'descripcion': idtipo1.IDtipo2.descripcion,
            'abreviatura': idtipo1.IDtipo2.abreviatura
        }
    else:
        idtipo2_data = None  # Si no tiene asociado un IDTipo2
    
    # Devolver los datos en formato JSON
    return JsonResponse({'idtipo2': idtipo2_data})


def calcular_cod_alpha(request):
    try:
        idtipo1_id = request.GET.get('idTipo1')
        idtipo2_id = request.GET.get('idTipo2')
        producto_id = request.GET.get('productoId')

        # Validación de parámetros
        if not (idtipo1_id and idtipo2_id and producto_id):
            return JsonResponse({'error': 'Faltan parámetros'}, status=400)

        # Obtén las instancias de Producto, IDTipo1 e IDTipo2
        producto = Producto.objects.get(id=producto_id)
        idtipo1 = IDTipo1.objects.get(id=idtipo1_id)
        idtipo2 = IDTipo2.objects.get(id=idtipo2_id)

        # Formatea el ID del producto a 7 caracteres con ceros a la izquierda
        producto_id_formateado = str(producto.id).zfill(7)

        # Lógica para calcular el código alpha
        cod_alpha = f"{idtipo1.cod_alpha}{idtipo2.cod_alpha}{producto_id_formateado}"

        # Devuelve la respuesta en formato JSON
        return JsonResponse({'cod_alpha': cod_alpha})

    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)
    except IDTipo1.DoesNotExist:
        return JsonResponse({'error': 'IDTipo1 no encontrado'}, status=404)
    except IDTipo2.DoesNotExist:
        return JsonResponse({'error': 'IDTipo2 no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Listar
class TipoIDTipo2ListView(ListView):
    model = TipoIDTipo2
    template_name = 'productos/tipoidtipo2_list.html'
    context_object_name = 'tipos'

# Crear
class TipoIDTipo2CreateView(CreateView):
    model = TipoIDTipo2
    form_class = TipoIDTipo2Form
    template_name = 'productos/tipoidtipo2_form.html'
    success_url = reverse_lazy('tipoidtipo2_list')

# Editar
class TipoIDTipo2UpdateView(UpdateView):
    model = TipoIDTipo2
    form_class = TipoIDTipo2Form
    template_name = 'productos/tipoidtipo2_form.html'
    success_url = reverse_lazy('tipoidtipo2_list')

# Eliminar
class TipoIDTipo2DeleteView(DeleteView):
    model = TipoIDTipo2
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('tipoidtipo2_list')


def get_idtipo1_details(request, idTipo1):
    try:
        # Obtener el objeto IDTipo1
        idtipo1 = IDTipo1.objects.get(pk=idTipo1)

        # Verificar si tiene un IDTipo2 asociado y obtener su descripción
        tipoidtipo2_descripcion = idtipo1.IDtipo2.descripcion if idtipo1.IDtipo2 else "---"

        # Devolver una respuesta JSON con datos serializables
        return JsonResponse({"idtipo2_descripcion": tipoidtipo2_descripcion})
    except IDTipo1.DoesNotExist:
        # Manejar el caso en que el idTipo1 no exista
        return JsonResponse({"idtipo2_descripcion": "---"}, status=404)
