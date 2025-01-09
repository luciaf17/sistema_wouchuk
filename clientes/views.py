from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import TipoDocumento
from .forms import TipoDocumentoForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'home.html')

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
    template_name = 'clientes/tipodocumento_confirm_delete.html'
    success_url = reverse_lazy('tipodocumento_list')
