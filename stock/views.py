# views.py
from django.db import models
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Deposito, Pasillo, Columna, Estante
from .forms import DepositoForm, PasilloForm, ColumnaForm, EstanteForm


from django.shortcuts import render
from remitos.models import DetalleRemito
from productos.models import Producto, Rubro, IDTipo1, IDTipo2
from django.db.models import Case, When, Value, F, IntegerField, Sum

from django.db.models import Sum, F, Case, When, IntegerField, Value, Q

class ConsultaStockView(ListView):
    model = Producto
    template_name = 'stock/consulta_stock.html'
    context_object_name = 'productos'

    def get_queryset(self):
        queryset = (
            Producto.objects
            .select_related('rubro')  # Relación directa
            .prefetch_related('desconcatenada__IDtipo1', 'desconcatenada__IDtipo2')  # Relación inversa
            .annotate(
                calculated_stock=Sum(
                    Case(
                        # Solo considerar remitos activos
                        When(detalleremito__remito__estado_remito='activo', then=Case(
                            # Compras aumentan el stock
                            When(detalleremito__remito__tipo_remito='compra', then=F('detalleremito__cantidad')),
                            # Ventas disminuyen el stock
                            When(detalleremito__remito__tipo_remito='venta', then=-F('detalleremito__cantidad')),
                            # Interdepósitos afectan origen y destino
                            When(
                                detalleremito__remito__tipo_remito='interdeposito',
                                then=Case(
                                    When(detalleremito__dep_origen__isnull=False, then=-F('detalleremito__cantidad')),
                                    When(detalleremito__dep_destino__isnull=False, then=F('detalleremito__cantidad')),
                                    default=Value(0),
                                    output_field=IntegerField(),
                                )
                            ),
                            default=Value(0),
                            output_field=IntegerField(),
                        )),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                )
            )
        )

        # Filtro por descripción o código de barras
        query = self.request.GET.get('q', '').strip()
        if query:
            palabras = query.split()
            q_filter = Q()
            for palabra in palabras:
                q_filter &= Q(descripcion__icontains=palabra) | Q(barcode__icontains=palabra)
            queryset = queryset.filter(q_filter)

        # Filtro por Rubro
        rubro = self.request.GET.get('rubro')
        if rubro:
            queryset = queryset.filter(rubro_id=rubro)

        # Filtro por Grupo (IDTipo1)
        grupo = self.request.GET.get('grupo')
        if grupo:
            queryset = queryset.filter(desconcatenada__IDtipo1_id=grupo)

        # Filtro por Subgrupo (IDTipo2)
        subgrupo = self.request.GET.get('subgrupo')
        if subgrupo:
            queryset = queryset.filter(desconcatenada__IDtipo2_id=subgrupo)

        # Filtro por Depósito
        deposito = self.request.GET.get('deposito')
        if deposito:
            queryset = queryset.filter(detalleremito__dep_destino_id=deposito)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubros'] = Rubro.objects.all()
        context['grupos'] = IDTipo1.objects.all()
        context['subgrupos'] = IDTipo2.objects.all()
        context['depositos'] = Deposito.objects.all()
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