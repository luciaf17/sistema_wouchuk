# views.py
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Deposito, Pasillo, Columna, Estante
from .forms import DepositoForm, PasilloForm, ColumnaForm, EstanteForm

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