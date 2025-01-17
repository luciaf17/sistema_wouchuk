import decimal
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.shortcuts import redirect, get_object_or_404
from .models import Remito, DetalleRemito
from .forms import RemitoForm, DetalleRemitoForm
from django.forms import modelformset_factory
from django.db import transaction
from productos.models import Producto
import json
from django.http import JsonResponse

class RemitoListView(ListView):
    model = Remito
    template_name = 'remitos/remito_list.html'
    context_object_name = 'remitos'

    def get_queryset(self):
        return Remito.objects.select_related('cliente', 'dep_origen', 'dep_destino').all()



class RemitoCreateView(CreateView):
    model = Remito
    form_class = RemitoForm
    template_name = 'remitos/remito_form.html'

    def form_valid(self, form):
        # Guardar el remito principal
        response = super().form_valid(form)

        # Procesar los detalles del remito
        detalles = self.request.POST.getlist('detalles[]')  # Capturar detalles enviados desde el formulario
        if detalles:
            try:
                with transaction.atomic():
                    for detalle in detalles:
                        data = json.loads(detalle)
                        print("Detalle recibido:", data)  # Agregar depuración para verificar datos
                        producto = Producto.objects.get(barcode=data['barcode'])
                        DetalleRemito.objects.create(
                            remito=self.object,
                            producto=producto,
                            cantidad=int(data['cantidad']),
                            precio_unit=float(data['precio_unit'])
                        )
            except Exception as e:
                print("Error al guardar detalles del remito:", e)  # Depuración de errores
                raise e
        return response

    def form_valid(self, form):
        # Save the main Remito object
        response = super().form_valid(form)
        
        # Process the detalles
        detalles_json = self.request.POST.get('detalles[]')  # Get the JSON string
        if detalles_json:
            try:
                detalles = json.loads(detalles_json)  # Deserialize JSON string into Python objects
                with transaction.atomic():
                    for detalle in detalles:
                        # Ensure all expected keys exist in each detalle
                        barcode = detalle.get('barcode')
                        cantidad = detalle.get('cantidad')
                        precio_unit = detalle.get('precio_unit')
                        
                        if not barcode or not cantidad or not precio_unit:
                            raise ValueError('Missing fields in detalle.')

                        producto = Producto.objects.get(barcode=barcode)
                        DetalleRemito.objects.create(
                            remito=self.object,
                            producto=producto,
                            cantidad=int(cantidad),
                            precio_unit=decimal.Decimal(precio_unit)
                        )
            except (ValueError, json.JSONDecodeError) as e:
                form.add_error(None, f"Error processing detalles: {e}")
                return self.form_invalid(form)
        return response



    def get_success_url(self):
        return reverse_lazy('remito_list')


class RemitoUpdateView(UpdateView):
    model = Remito
    form_class = RemitoForm
    template_name = 'remitos/remito_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener detalles relacionados con el remito actual
        context['detalle_remito'] = DetalleRemito.objects.filter(remito=self.object)
        return context

    def form_valid(self, form):
        response = super().form_valid(form)

        # Procesar los detalles actualizados
        detalles_json = self.request.POST.get('detalles[]')
        if detalles_json:
            try:
                detalles = json.loads(detalles_json)  # Deserializar JSON
                with transaction.atomic():
                    # Eliminar detalles existentes para reemplazar por los nuevos
                    DetalleRemito.objects.filter(remito=self.object).delete()
                    for detalle in detalles:
                        barcode = detalle.get('barcode')
                        cantidad = detalle.get('cantidad')
                        precio_unit = detalle.get('precio_unit')

                        if not barcode or not cantidad or not precio_unit:
                            raise ValueError('Missing fields in detalle.')

                        producto = Producto.objects.get(barcode=barcode)
                        DetalleRemito.objects.create(
                            remito=self.object,
                            producto=producto,
                            cantidad=int(cantidad),
                            precio_unit=decimal.Decimal(precio_unit)
                        )
            except (ValueError, json.JSONDecodeError) as e:
                form.add_error(None, f"Error processing detalles: {e}")
                return self.form_invalid(form)
        return response

    def get_success_url(self):
        return reverse_lazy('remito_list')


def remito_anular(request, pk):
    remito = get_object_or_404(Remito, pk=pk)
    remito.estado_remito = 'anulado'
    remito.save()
    return redirect('remito_list')


def remito_activar(request, pk):
    remito = get_object_or_404(Remito, pk=pk)
    remito.estado_remito = 'activo'
    remito.save()
    return redirect('remito_list')