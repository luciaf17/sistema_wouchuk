from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import TipoDocumento, CategoriaArca, Rubro, Departamento, TipoCliente, Pais, Provincia, Localidad, Cliente, ClienteTipo, Contacto
from .forms import TipoDocumentoForm, CategoriaArcaForm, RubroForm, DepartamentoForm, TipoClienteForm, PaisForm, ProvinciaForm, LocalidadForm, ClienteForm, ClienteTipoForm, ContactoForm, ClienteTipoFormSet
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

#este decorador hace que se requiera login en toda la app
@login_required
def home(request):
    return render(request, 'home.html')

#vistas para tipo de documento
class TipoDocumentoListView(ListView):
    model = TipoDocumento
    template_name = 'clientes/tipodocumento_list.html'
    context_object_name = 'tipodocumentos'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return TipoDocumento.objects.filter(descripcion__icontains=query)
        return TipoDocumento.objects.all()

class TipoDocumentoCreateView(CreateView):
    model = TipoDocumento
    form_class = TipoDocumentoForm
    template_name = 'clientes/tipodocumento_form.html'
    success_url = reverse_lazy('tipodocumento_list')

class TipoDocumentoUpdateView(UpdateView):
    model = TipoDocumento
    form_class = TipoDocumentoForm
    template_name = 'clientes/tipodocumento_form.html'
    success_url = reverse_lazy('tipodocumento_list')

class TipoDocumentoDeleteView(DeleteView):
    model = TipoDocumento
    template_name = 'confirm_delete.html'  # Nuevo template genérico
    success_url = reverse_lazy('tipodocumento_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'tipo de documento'  # Título dinámico
        context['cancel_url'] = reverse_lazy('tipodocumento_list')  # URL para el botón "Cancelar"
        return context

#Vistas para CategoriaArca

class CategoriaArcaListView(ListView):
    model = CategoriaArca
    template_name = 'clientes/categoriaarca_list.html'
    context_object_name = 'categorias'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return CategoriaArca.objects.filter(descripcion__icontains=query)
        return CategoriaArca.objects.all()

class CategoriaArcaCreateView(CreateView):
    model = CategoriaArca
    form_class = CategoriaArcaForm
    template_name = 'clientes/categoriaarca_form.html'
    success_url = reverse_lazy('categoriaarca_list')

class CategoriaArcaUpdateView(UpdateView):
    model = CategoriaArca
    form_class = CategoriaArcaForm
    template_name = 'clientes/categoriaarca_form.html'
    success_url = reverse_lazy('categoriaarca_list')

class CategoriaArcaDeleteView(DeleteView):
    model = CategoriaArca
    template_name = 'confirm_delete.html'  # Template genérico
    success_url = reverse_lazy('categoriaarca_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'categoría arca'
        context['cancel_url'] = reverse_lazy('categoriaarca_list')
        return context
    

#Vistas para Rubros

class RubroListView(ListView):
    model = Rubro
    template_name = 'clientes/rubro_list.html'
    context_object_name = 'rubros'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Rubro.objects.filter(descripcion__icontains=query)
        return Rubro.objects.all()

class RubroCreateView(CreateView):
    model = Rubro
    form_class = RubroForm
    template_name = 'clientes/rubro_form.html'
    success_url = reverse_lazy('rubro_list')

class RubroUpdateView(UpdateView):
    model = Rubro
    form_class = RubroForm
    template_name = 'clientes/rubro_form.html'
    success_url = reverse_lazy('rubro_list')

class RubroDeleteView(DeleteView):
    model = Rubro
    template_name = 'confirm_delete.html'  # Reutilizamos el template genérico
    success_url = reverse_lazy('rubro_list')


class DepartamentoListView(ListView):
    model = Departamento
    template_name = 'clientes/departamento_list.html'
    context_object_name = 'departamentos'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Departamento.objects.filter(descripcion__icontains=query)
        return Departamento.objects.all()

class DepartamentoCreateView(CreateView):
    model = Departamento
    form_class = DepartamentoForm
    template_name = 'clientes/departamento_form.html'
    success_url = reverse_lazy('departamento_list')

class DepartamentoUpdateView(UpdateView):
    model = Departamento
    form_class = DepartamentoForm
    template_name = 'clientes/departamento_form.html'
    success_url = reverse_lazy('departamento_list')

class DepartamentoDeleteView(DeleteView):
    model = Departamento
    template_name = 'confirm_delete.html'  # Reutilizamos el template genérico
    success_url = reverse_lazy('departamento_list')

class TipoClienteListView(ListView):
    model = TipoCliente
    template_name = 'clientes/tipocliente_list.html'
    context_object_name = 'tipoclientes'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return TipoCliente.objects.filter(descripcion__icontains=query)
        return TipoCliente.objects.all()

class TipoClienteCreateView(CreateView):
    model = TipoCliente
    form_class = TipoClienteForm
    template_name = 'clientes/tipocliente_form.html'
    success_url = reverse_lazy('tipocliente_list')

class TipoClienteUpdateView(UpdateView):
    model = TipoCliente
    form_class = TipoClienteForm
    template_name = 'clientes/tipocliente_form.html'
    success_url = reverse_lazy('tipocliente_list')

class TipoClienteDeleteView(DeleteView):
    model = TipoCliente
    template_name = 'confirm_delete.html'  # Reutilizamos el template genérico
    success_url = reverse_lazy('tipocliente_list')

class PaisListView(ListView):
    model = Pais
    template_name = 'clientes/pais_list.html'
    context_object_name = 'paises'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Pais.objects.filter(descripcion__icontains=query)
        return Pais.objects.all()

class PaisCreateView(CreateView):
    model = Pais
    form_class = PaisForm
    template_name = 'clientes/pais_form.html'
    success_url = reverse_lazy('pais_list')

class PaisUpdateView(UpdateView):
    model = Pais
    form_class = PaisForm
    template_name = 'clientes/pais_form.html'
    success_url = reverse_lazy('pais_list')

class PaisDeleteView(DeleteView):
    model = Pais
    template_name = 'confirm_delete.html'  # Reutilizamos el template genérico
    success_url = reverse_lazy('pais_list')

class ProvinciaListView(ListView):
    model = Provincia
    template_name = 'clientes/provincia_list.html'
    context_object_name = 'provincias'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Provincia.objects.filter(descripcion__icontains=query)
        return Provincia.objects.all()

class ProvinciaCreateView(CreateView):
    model = Provincia
    form_class = ProvinciaForm
    template_name = 'clientes/provincia_form.html'
    success_url = reverse_lazy('provincia_list')

class ProvinciaUpdateView(UpdateView):
    model = Provincia
    form_class = ProvinciaForm
    template_name = 'clientes/provincia_form.html'
    success_url = reverse_lazy('provincia_list')

class ProvinciaDeleteView(DeleteView):
    model = Provincia
    template_name = 'confirm_delete.html'  # Reutilizamos el template genérico
    success_url = reverse_lazy('provincia_list')

class LocalidadListView(ListView):
    model = Localidad
    template_name = 'clientes/localidad_list.html'
    context_object_name = 'localidades'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Localidad.objects.filter(descripcion__icontains=query)
        return Localidad.objects.all()

class LocalidadCreateView(CreateView):
    model = Localidad
    form_class = LocalidadForm
    template_name = 'clientes/localidad_form.html'
    success_url = reverse_lazy('localidad_list')

class LocalidadUpdateView(UpdateView):
    model = Localidad
    form_class = LocalidadForm
    template_name = 'clientes/localidad_form.html'
    success_url = reverse_lazy('localidad_list')

class LocalidadDeleteView(DeleteView):
    model = Localidad
    template_name = 'confirm_delete.html'  # Reutilizamos el template genérico
    success_url = reverse_lazy('localidad_list')

class ClienteListView(ListView):
    model = Cliente
    template_name = 'clientes/cliente_list.html'
    context_object_name = 'clientes'

    def get_queryset(self):
        query = self.request.GET.get('q')
        tipo_cliente = self.request.GET.get('tipo_cliente')
        clientes = Cliente.objects.all()

        if query:
            clientes = clientes.filter(descripcion__icontains=query)

        if tipo_cliente:
            clientes = clientes.filter(tipos__tipo_cliente_id=tipo_cliente, tipos__principal=True)

        return clientes.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos_cliente'] = TipoCliente.objects.all()
        context['clientes_principal'] = {
            cliente.id: cliente.tipos.filter(principal=True).first().tipo_cliente.descripcion
            if cliente.tipos.filter(principal=True).exists()
            else "N/A"
            for cliente in self.get_queryset()
        }
        return context


class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/cliente_form.html'
    success_url = reverse_lazy('cliente_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos_cliente'] = TipoCliente.objects.all()
        context['cliente_tipos'] = []  # No hay tipos de cliente porque es creación
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        tipos_cliente = self.request.POST.getlist('tipos_cliente')
        principal_id = self.request.POST.get('tipo_principal')
        for tipo_id in tipos_cliente:
            ClienteTipo.objects.create(
                cliente=self.object,
                tipo_cliente_id=tipo_id,
                principal=(tipo_id == principal_id)
            )
        return response


class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/cliente_form.html'
    success_url = reverse_lazy('cliente_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos_cliente'] = TipoCliente.objects.all()
        context['cliente_tipos'] = ClienteTipo.objects.filter(cliente=self.object)
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        ClienteTipo.objects.filter(cliente=self.object).delete()
        tipos_cliente = self.request.POST.getlist('tipos_cliente')
        principal_id = self.request.POST.get('tipo_principal')
        for tipo_id in tipos_cliente:
            ClienteTipo.objects.create(
                cliente=self.object,
                tipo_cliente_id=tipo_id,
                principal=(tipo_id == principal_id)
            )
        return response

    
class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('cliente_list')

class ClienteTipoCreateView(CreateView):
    model = ClienteTipo
    form_class = ClienteTipoForm
    template_name = 'clientes/clientetipo_form.html'
    success_url = reverse_lazy('cliente_list')  # Retorna a la lista de clientes

class ClienteTipoDeleteView(DeleteView):
    model = ClienteTipo
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('cliente_list')


class ContactoListView(ListView):
    model = Contacto
    template_name = 'clientes/contacto_list.html'
    context_object_name = 'contactos'

    def get_queryset(self):
        cliente_id = self.kwargs.get('cliente_id')
        return Contacto.objects.filter(cliente_id=cliente_id)

class ContactoCreateView(CreateView):
    model = Contacto
    form_class = ContactoForm
    template_name = 'clientes/contacto_form.html'

    def get_success_url(self):
        return reverse_lazy('contacto_list', kwargs={'cliente_id': self.object.cliente.id})

    def get_initial(self):
        initial = super().get_initial()
        cliente_id = self.kwargs.get('cliente_id')
        initial['cliente'] = cliente_id
        return initial

class ContactoUpdateView(UpdateView):
    model = Contacto
    form_class = ContactoForm
    template_name = 'clientes/contacto_form.html'

    def get_success_url(self):
        return reverse_lazy('contacto_list', kwargs={'cliente_id': self.object.cliente.id})

class ContactoDeleteView(DeleteView):
    model = Contacto
    template_name = 'confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('contacto_list', kwargs={'cliente_id': self.object.cliente.id})