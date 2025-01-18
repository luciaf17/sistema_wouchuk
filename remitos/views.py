import decimal
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.shortcuts import redirect, get_object_or_404
from .models import Remito, DetalleRemito
from clientes.models import Cliente
from .forms import RemitoForm, DetalleRemitoForm
from django.forms import modelformset_factory
from django.db import transaction
from productos.models import Producto
import json
from django.http import JsonResponse
import os
from fpdf import FPDF
from django.utils.timezone import localtime
from math import ceil
from django.http import FileResponse
from datetime import datetime, timedelta
from django.utils.timezone import make_aware

class RemitoListView(ListView):
    model = Remito
    template_name = 'remitos/remito_list.html'
    context_object_name = 'remitos'

    def get_queryset(self):
        queryset = Remito.objects.select_related('cliente', 'dep_origen', 'dep_destino').all()

        # Obtener los parámetros de filtro
        fecha_desde = self.request.GET.get('fecha_desde')
        fecha_hasta = self.request.GET.get('fecha_hasta')
        cliente = self.request.GET.get('cliente')
        tipo_remito = self.request.GET.get('tipo_remito')

        # Filtro por fecha desde (inicio del día)
        if fecha_desde:
            try:
                fecha_desde_dt = make_aware(datetime.strptime(fecha_desde, '%Y-%m-%d'))
                queryset = queryset.filter(fecha__gte=fecha_desde_dt)
            except ValueError:
                print(f"Fecha desde inválida: {fecha_desde}")

        # Filtro por fecha hasta (final del día)
        if fecha_hasta:
            try:
                fecha_hasta_dt = make_aware(datetime.strptime(fecha_hasta, '%Y-%m-%d') + timedelta(days=1) - timedelta(seconds=1))
                queryset = queryset.filter(fecha__lte=fecha_hasta_dt)
            except ValueError:
                print(f"Fecha hasta inválida: {fecha_hasta}")

        # Filtro por cliente
        if cliente:
            queryset = queryset.filter(cliente_id=cliente)

        # Filtro por tipo de remito
        if tipo_remito:
            queryset = queryset.filter(tipo_remito=tipo_remito)


        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clientes'] = Cliente.objects.all()
        context['remito_tipos'] = Remito._meta.get_field('tipo_remito').choices
        return context

def generar_pdf_remito(remito, detalles):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Configuración de fuentes
    pdf.set_font('Helvetica', 'B', 12)  # Fuente en negrita para títulos

    # Agregar el logo
    logo_path = "static/wouchuk-logo.jpg"
    if os.path.exists(logo_path):
        pdf.image(logo_path, x=10, y=8, w=33)  # Ajusta las coordenadas y el tamaño del logo
    else:
        print(f"Error: No se encontró el logo en la ruta {logo_path}")

    # Encabezado
    remito_id_formateado = f"{remito.id:08d}"  # Formatear con ceros a la izquierda
    pdf.cell(200, 10, f"Remito - #{remito_id_formateado}", ln=True, align="C")
    pdf.ln(10)

    # Detalles del remito
    pdf.set_font('Helvetica', '', 10)  # Fuente regular para detalles
    pdf.cell(200, 10, f"Fecha: {localtime(remito.fecha).strftime('%d/%m/%Y %H:%M')}", ln=True, align="R")
    pdf.cell(200, 10, f"Tipo: {remito.get_tipo_remito_display()}", ln=True, align="L")
    pdf.cell(200, 10, f"Cliente: {remito.cliente or '-'}", ln=True, align="L")
    pdf.cell(200, 10, f"Depósito Origen: {remito.dep_origen or '-'}", ln=True, align="L")
    pdf.cell(200, 10, f"Depósito Destino: {remito.dep_destino or '-'}", ln=True, align="L")
    pdf.ln(10)

    # Configuración de la tabla
    pdf.set_fill_color(0, 150, 0)  # Color verde para el encabezado
    pdf.set_text_color(255, 255, 255)  # Texto blanco para el encabezado
    pdf.set_font('Helvetica', 'B', 8)  # Fuente en negrita para encabezados
    pdf.cell(20, 10, "Código", border=1, align="C", fill=True)
    pdf.cell(40, 10, "Barcode", border=1, align="C", fill=True)
    pdf.cell(70, 10, "Descripción", border=1, align="C", fill=True)
    pdf.cell(20, 10, "Cantidad", border=1, align="C", fill=True)
    pdf.cell(30, 10, "Precio Unit.", border=1, align="C", fill=True)
    pdf.ln()

    # Filas
    pdf.set_text_color(0, 0, 0)  # Texto negro para las filas
    pdf.set_font('Helvetica', '', 8)  # Fuente regular para las filas
    for detalle in detalles:
        pdf.cell(20, 10, str(detalle.id), border=1, align="C")  # ID del detalle
        pdf.cell(40, 10, detalle.producto.barcode, border=1, align="C")  # Código de barras
        pdf.cell(70, 10, detalle.producto.descripcion, border=1, align="L")
        pdf.cell(20, 10, str(detalle.cantidad), border=1, align="C")
        pdf.cell(30, 10, f"${detalle.precio_unit:.2f}", border=1, align="R")
        pdf.ln()

    # Guardar PDF
    pdf_dir = "static/remitos"
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)

    pdf_path = os.path.join(pdf_dir, f"remito_{remito_id_formateado}.pdf")
    pdf.output(pdf_path)
    return pdf_path



class RemitoCreateView(CreateView):
    model = Remito
    form_class = RemitoForm
    template_name = 'remitos/remito_form.html'

    def form_valid(self, form):
        # Guardar el remito principal
        response = super().form_valid(form)

        # Procesar los detalles del remito
        detalles_json = self.request.POST.get('detalles[]')
        if detalles_json:
            try:
                detalles = json.loads(detalles_json)
                with transaction.atomic():
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

        # Generar el PDF
        detalles_remito = DetalleRemito.objects.filter(remito=self.object)
        pdf_path = generar_pdf_remito(self.object, detalles_remito)

        # Retornar el PDF como respuesta
        return FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')


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

        # Generar el PDF
        detalles_remito = DetalleRemito.objects.filter(remito=self.object)
        pdf_path = generar_pdf_remito(self.object, detalles_remito)

        # Retornar el PDF en una nueva pestaña
        try:
            # Usar `FileResponse` para servir el archivo
            pdf_file = open(pdf_path, 'rb')  # Abrir sin `with` para evitar que se cierre automáticamente
            response = FileResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="remito_{str(self.object.id).zfill(6)}.pdf"'
            return response
        except Exception as e:
            form.add_error(None, f"Error al generar o abrir el PDF: {str(e)}")
            return self.form_invalid(form)

    def get_success_url(self):
        # Redirigir al listado de remitos si el PDF no se genera correctamente
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