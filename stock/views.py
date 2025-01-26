# views.py
from django.db import models
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Deposito, Pasillo, Columna, Estante, Stock
from .forms import DepositoForm, PasilloForm, ColumnaForm, EstanteForm


from django.shortcuts import render
from remitos.models import DetalleRemito
from productos.models import Producto, Rubro, IDTipo1, IDTipo2
from django.db.models import Case, When, Value, F, IntegerField, Sum

from django.db.models import Sum, F, Case, When, IntegerField, Value, Q

from django.db.models import Q
from django.views.generic import ListView, DetailView
from .models import Deposito, Stock
from productos.models import Producto, Rubro, IDTipo1, IDTipo2

from django.db.models import F, Sum, Q

class ConsultaStockView(ListView):
    model = Stock
    template_name = 'stock/consulta_stock.html'
    context_object_name = 'stocks'

    def get_queryset(self):
    # Excluir depósitos "Compras" y "Ventas" de la consulta general
        exclude_depositos = Deposito.objects.filter(descripcion__in=["Compras", "Ventas"]).values_list('id', flat=True)
        
        queryset = Stock.objects.select_related('producto', 'deposito').exclude(deposito_id__in=exclude_depositos)

        # Filtro por descripción o código de barras
        query = self.request.GET.get('q', '').strip()
        if query:
            palabras = query.split()
            q_filter = Q()
            for palabra in palabras:
                q_filter &= Q(producto__descripcion__icontains=palabra) | Q(producto__barcode__icontains=palabra)
            queryset = queryset.filter(q_filter)

        # Filtro por rubro, grupo, subgrupo
        rubro = self.request.GET.get('rubro')
        if rubro:
            queryset = queryset.filter(producto__rubro_id=rubro)

        grupo = self.request.GET.get('grupo')
        if grupo:
            queryset = queryset.filter(producto__desconcatenada__IDtipo1_id=grupo)

        subgrupo = self.request.GET.get('subgrupo')
        if subgrupo:
            queryset = queryset.filter(producto__desconcatenada__IDtipo2_id=subgrupo)

        deposito = self.request.GET.get('deposito')
        if deposito:
            # Filtrar por depósito específico
            queryset = queryset.filter(deposito_id=deposito)
        else:
            # Agrupar por producto para calcular cantidad total
            queryset = (
                queryset.values(
                    'producto__id',
                    'producto__descripcion',
                    'producto__barcode',
                    'producto__rubro__descripcion',
                    'producto__desconcatenada__IDtipo1__descripcion',
                    'producto__desconcatenada__IDtipo2__descripcion',
                )
                .annotate(total_cantidad=Sum('cantidad'))
                .order_by('producto__id')
            )

        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubros'] = Rubro.objects.all()
        context['grupos'] = IDTipo1.objects.all()
        context['subgrupos'] = IDTipo2.objects.all()
        context['depositos'] = Deposito.objects.all()
        return context

class ProductoDepositoDetailView(DetailView):
    model = Producto
    template_name = 'stock/producto_deposito_detail.html'
    context_object_name = 'producto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Excluir depósitos "Compras" y "Ventas"
        context['stocks'] = Stock.objects.filter(
            producto=self.object
        ).exclude(
            deposito__descripcion__in=["Compras", "Ventas"]
        ).select_related('deposito')
        return context


class DepositoListView(ListView):
    model = Deposito
    template_name = 'stock/deposito_list.html'
    context_object_name = 'depositos'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Deposito.objects.filter(descripcion__icontains=query)
        return Deposito.objects.all()

class DepositoCreateView(CreateView):
    model = Deposito
    form_class = DepositoForm
    template_name = 'stock/deposito_form.html'
    success_url = reverse_lazy('deposito_list')

class DepositoUpdateView(UpdateView):
    model = Deposito
    form_class = DepositoForm
    template_name = 'stock/deposito_form.html'
    success_url = reverse_lazy('deposito_list')

class DepositoDeleteView(DeleteView):
    model = Deposito
    template_name = 'confirm_delete.html'  # Usamos un template genérico
    success_url = reverse_lazy('deposito_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'depósito'
        context['cancel_url'] = reverse_lazy('deposito_list')  # URL para el botón "Cancelar"
        return context


# Pasillo
class PasilloListView(ListView):
    model = Pasillo
    template_name = 'stock/pasillo_list.html'
    context_object_name = 'pasillos'


class PasilloCreateView(CreateView):
    model = Pasillo
    form_class = PasilloForm
    template_name = 'stock/pasillo_form.html'
    success_url = reverse_lazy('pasillo_list')


class PasilloUpdateView(UpdateView):
    model = Pasillo
    form_class = PasilloForm
    template_name = 'stock/pasillo_form.html'
    success_url = reverse_lazy('pasillo_list')


class PasilloDeleteView(DeleteView):
    model = Pasillo
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('pasillo_list')

# Columna
class ColumnaListView(ListView):
    model = Columna
    template_name = 'stock/columna_list.html'
    context_object_name = 'columnas'


class ColumnaCreateView(CreateView):
    model = Columna
    form_class = ColumnaForm
    template_name = 'stock/columna_form.html'
    success_url = reverse_lazy('columna_list')


class ColumnaUpdateView(UpdateView):
    model = Columna
    form_class = ColumnaForm
    template_name = 'stock/columna_form.html'
    success_url = reverse_lazy('columna_list')


class ColumnaDeleteView(DeleteView):
    model = Columna
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('columna_list')

# Estante
class EstanteListView(ListView):
    model = Estante
    template_name = 'stock/estante_list.html'
    context_object_name = 'estantes'


class EstanteCreateView(CreateView):
    model = Estante
    form_class = EstanteForm
    template_name = 'stock/estante_form.html'
    success_url = reverse_lazy('estante_list')


class EstanteUpdateView(UpdateView):
    model = Estante
    form_class = EstanteForm
    template_name = 'stock/estante_form.html'
    success_url = reverse_lazy('estante_list')


class EstanteDeleteView(DeleteView):
    model = Estante
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('estante_list')